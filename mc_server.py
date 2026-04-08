"""
KittenSMP Fake Minecraft Server
- Responds to server list pings (shows online, player count, MOTD)
- Kicks anyone who tries to join with a download message
Run: python3 mc_server.py
"""

import socket
import json
import threading

MC_VERSION      = "1.20.4"
MC_PROTOCOL     = 765
PLAYERS_ONLINE  = 147
PLAYERS_MAX     = 500
MOTD            = "§d§lKitten SMP §r§7| §fSeason 1 • Blossom ✨"
DISCONNECT_MSG  = (
    '{"text":"§c✖ §fThis server requires the §bKitten Client§f!\\n'
    '§7Please download it at: §awww.kittensmp.com"}'
)
PORT            = 25565

def write_varint(value: int) -> bytes:
    buf = b""
    while True:
        part = value & 0x7F
        value >>= 7
        if value:
            part |= 0x80
        buf += bytes([part])
        if not value:
            return buf


def read_varint(data: bytes, offset: int = 0):
    result, shift = 0, 0
    while offset < len(data):
        b = data[offset]; offset += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, offset
        shift += 7
    raise ValueError("Truncated varint")


def make_packet(packet_id: int, payload: bytes) -> bytes:
    body = write_varint(packet_id) + payload
    return write_varint(len(body)) + body


def recv_all(conn: socket.socket, length: int) -> bytes:
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            break
        data += chunk
    return data


def handle_client(conn: socket.socket, addr):
    try:
        conn.settimeout(8)
        raw = b""

        # ── Read handshake packet ──────────────────────────
        # First 5 bytes are enough to get the length varint
        raw = conn.recv(512)
        if not raw:
            return

        pkt_len, off = read_varint(raw, 0)
        pkt_id,  off = read_varint(raw, off)

        if pkt_id != 0x00:          # not a handshake
            return

        # Read client's protocol version (echo it back for multi-version compat)
        client_protocol, off = read_varint(raw, off)

        # Skip: server address string (varint len + bytes)
        str_len, off = read_varint(raw, off)
        off += str_len

        # Skip: server port (unsigned short, 2 bytes)
        off += 2

        # Next state
        next_state, _ = read_varint(raw, off)

        # ── STATUS (server list ping) ──────────────────────
        if next_state == 1:
            conn.recv(2)                # eat status-request packet

            status = {
                "version": {"name": "1.20.1 - 1.21.5", "protocol": client_protocol},
                "players": {"max": PLAYERS_MAX, "online": PLAYERS_ONLINE, "sample": []},
                "description": {"text": MOTD}
            }
            status_bytes = json.dumps(status, ensure_ascii=False).encode("utf-8")
            payload = write_varint(len(status_bytes)) + status_bytes
            conn.sendall(make_packet(0x00, payload))

            # Echo the ping packet back
            ping = conn.recv(10)
            if ping:
                conn.sendall(ping)

        # ── LOGIN (someone actually trying to join) ────────
        elif next_state == 2:
            conn.recv(512)              # eat login-start packet

            msg_bytes = DISCONNECT_MSG.encode("utf-8")
            payload   = write_varint(len(msg_bytes)) + msg_bytes
            conn.sendall(make_packet(0x00, payload))   # 0x00 = Login Disconnect


    except Exception:
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(64)
    print(f"[KittenSMP] Fake MC server listening on :{PORT}")

    while True:
        conn, addr = srv.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    main()

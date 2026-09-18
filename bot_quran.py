import os
import random
from datetime import datetime

import requests
import telebot

# ╔══════════════════════════════════════════════════════════════╗
# ║  ⚡ MHD QURAN BOT // MODERN HACKER MODE                    ║
# ║  ◈ Daily Quran automation • Secure webhook transmission    ║
# ╚══════════════════════════════════════════════════════════════╝

# --- ⚙️ KONFIGURASI SISTEM ---
TOKEN = os.getenv("BOT_TOKEN")
URL_MAKE = os.getenv("MAKE_WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)

# --- 🎨 UI TERMINAL ---
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"


def log(symbol, message, color=CYAN):
    """Cetak log bergaya terminal modern."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{DIM}[{timestamp}]{RESET} {color}{symbol}{RESET} {message}")


def get_content():
    try:
        # Ambil angka hari (0=Senin, 3=Kamis, 4=Jumat)
        hari_ini = datetime.now().weekday()

        if hari_ini == 4:
            # Mode Jumat: Al-Kahfi (Ayat 1-110)
            ayat_id = random.randint(1, 110)
            url = (
                "https://api.alquran.cloud/v1/ayah/"
                f"18:{ayat_id}/editions/quran-uthmani,id.indonesian"
            )
            prefix = "🕌 <b>[ JUMAT BERKAH // AL-KAHFI ]</b>"
            mode = "JUMAT BERKAH"
        else:
            # Mode biasa: ayat diacak dari seluruh Al-Qur'an
            ayat_id = random.randint(1, 6236)
            url = (
                "https://api.alquran.cloud/v1/ayah/"
                f"{ayat_id}/editions/quran-uthmani,id.indonesian"
            )
            prefix = "⚡ <b>[ MHD DAILY QURAN // RANDOM VERSE ]</b>"
            mode = "DAILY RANDOM"

        log("◈", f"Mode aktif : {mode}")
        log("↯", f"Request API : ayat #{ayat_id}", CYAN)

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200:
            arab = data["data"][0]["text"]
            arti = data["data"][1]["text"]
            surah = data["data"][0]["surah"]["englishName"]
            nomor = data["data"][0]["numberInSurah"]

            pesan = (
                f"{prefix}\n\n"
                f"🔐 <i>{arab}</i>\n\n"
                f"💬 <i>\"{arti}\"</i>\n\n"
                f"╭─ <b>VERSE DATA</b> ─╮\n"
                f"│ 📌 <b>QS. {surah} [{nomor}]</b>\n"
                f"│ 🧬 <b>STATUS:</b> VERIFIED\n"
                f"╰────────────────╯\n\n"
                f"📡 <b>Channel:</b> t.me/autoposting_quran\n"
                f"🌐 <b>Page:</b> fb.com/RuntimeIman\n\n"
                f"#AlQuran #SelfReminder #DailyVerse #RuntimeIman #MHDWarrior"
            )
            log("✓", f"Payload siap : {surah} [{nomor}]", GREEN)
            return pesan

        log("!", f"API mengembalikan kode tidak valid: {data.get('code')}", YELLOW)
    except Exception as e:
        log("✗", f"Error saat mengambil konten: {e}", RED)
    return None


if __name__ == "__main__":
    print()
    print(f"{GREEN}╔══════════════════════════════════════════════════════════════╗")
    print("║  ⚡ MHD VIRTUAL WARRIOR // SYSTEM ONLINE                   ║")
    print("╚══════════════════════════════════════════════════════════════╝" + RESET)

    ayat = get_content()

    if ayat:
        try:
            headers = {"Content-Type": "application/json"}
            payload = {"text": ayat}

            log("⇢", "Mengirim payload ke Make webhook...")
            res = requests.post(
                URL_MAKE,
                json=payload,
                headers=headers,
                timeout=10,
            )

            if res.status_code == 200:
                log("✓", f"Webhook status: {res.status_code} // DELIVERED", GREEN)
                log("★", "Misi berhasil: pesan mendarat di target.", GREEN)
            else:
                log("!", f"Webhook diterima tetapi bermasalah: {res.status_code}", YELLOW)
                log("↳", f"Response: {res.text}", YELLOW)

        except Exception as e:
            log("✗", f"Gagal kirim ke webhook: {e}", RED)
    else:
        log("✗", "Misi gagal: variabel ayat kosong.", RED)

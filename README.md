# DAWN Internet
Validasi akun DAWN Internet Validator Extension, Keep Alive Connection, cek all poin, dan mengirimkan notifikasi ke Telegram.

## Instalasi
1. **Clone Repository**
   ```bash
   git clone https://github.com/officialputuid/DAWNinternet dawn
   cd dawn
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfigurasi**
   Edit file `config.json` dengan format:
   ```json
   {
     "telegram_bot_token": "YOUR_TOKEN",
     "telegram_chat_id": "YOUR_CHAT_ID",
     "accounts": [
       {
         "email": "example@domain.com",
         "token": "YOUR_TOKEN"
       },
       {
         "email": "example@domain.com",
         "token": "YOUR_TOKEN"
       }
     ]
   }
   ```
   - `telegram_bot_token`: Token bot Telegram yang diperoleh dari @BotFather.
   - `telegram_chat_id`: ID chat Telegram yang diperoleh dari @getmyid_bot.
   - `accounts`: Daftar akun yang akan diproses. Masing-masing akun memerlukan `email` dan `token` yang didapat dari inspeksi jaringan.

4. **Jalankan skrip**
```bash
python dawn.py
```

## Cara Mendapatkan Token
1. **Klik Kanan dan Pilih "Inspect"** pada halaman DAWN Validator Extension.
2. **Pilih Tab "Network"**. Refresh halaman jika perlu.
3. **Cari Permintaan `getpoint`** dan klik pada permintaan tersebut.
4. **Salin Header `Authorization`** dan hapus kata "Bearer" di depan token.
5. **Gunakan Token** dalam file `config.json` pada bagian `token`.

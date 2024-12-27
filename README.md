# LSP Welcome Bot

Discord bot yang menyambut member baru dengan GIF dan pesan welcome yang kustom.

## Fitur

- Mengirim pesan welcome dengan embed
- Menampilkan avatar member di tengah GIF welcome
- Berjalan 24/7 menggunakan GitHub Actions

## Setup

1. Fork repository ini
2. Di repository GitHub Anda:
   - Buka Settings > Secrets and Variables > Actions
   - Klik "New repository secret"
   - Nama: `DISCORD_TOKEN`
   - Value: [Token bot Discord Anda]
   - Klik "Add secret"
3. Aktifkan GitHub Actions:
   - Buka tab Actions
   - Klik "I understand my workflows, go ahead and enable them"

## Penggunaan

- Bot akan otomatis menyambut member baru
- Gunakan command `!testwelcome` untuk test pesan welcome

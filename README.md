# Yang-Punya-Server
Discord Bot


# 🤖 Yang Punya Server Discord Bot

Bot Discord ini mendukung fitur **welcome**, **goodbye**, **ban message**, **announcement**, serta sistem **button role** dan **kontrol admin/staff**.

---

## ⚙️ Prefix
Prefix default: `^`  
Untuk mengubah prefix, kamu bisa sesuaikan bagian ini di `bot = commands.Bot(...)`:
```python
bot = commands.Bot(command_prefix="^", intents=intents)

| Command                    | Fungsi                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| `^set_welcome #channel`    | Mengatur channel untuk pesan selamat datang saat member baru join.                         |
| `^set_goodbye #channel`    | Mengatur channel untuk pesan perpisahan saat member keluar.                                |
| `^set_ban #channel`        | Mengatur channel untuk pesan saat member dibanned.                                         |
| `^set_announce #channel`   | Mengatur channel tempat bot akan mengirim pengumuman.                                      |
| `^set_control #channel`    | Mengatur channel khusus tempat admin/staff bisa menjalankan command seperti `announce`.    |
| `^set_roles`               | Mengirim pesan berisi tombol untuk memilih role tertentu (contoh: Member).                 |
| `^test_welcome`            | Mengirim pesan welcome ke channel yang diatur untuk keperluan uji coba.                    |
| `^test_goodbye`            | Mengirim pesan goodbye ke channel yang diatur untuk keperluan uji coba.                    |
| `^test_ban`                | Mengirim pesan ban ke channel yang diatur untuk keperluan uji coba.                        |
| `^announce Judul \| Pesan` | Mengirim pengumuman ke channel yang sudah diset sebelumnya. Hanya bisa dipakai oleh admin. |

| Command        | Akses Dibutuhkan                                  |
| -------------- | ------------------------------------------------- |
| Semua `^set_*` | Admin (punya izin `Manage Server`)                |
| `^test_*`      | Admin                                             |
| `^announce`    | Admin dan harus dijalankan di channel kontrol     |
| `^set_roles`   | Admin atau Staff (berdasarkan role ID dalam kode) |


---

Jika kamu menyimpannya sebagai `README.md`, GitHub akan otomatis menampilkannya di halaman utama repositori. Perlu bantuan untuk mengatur repositori GitHub atau deploy ke hosting (seperti Replit, Railway, dsb)?

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

---
📌 Fitur Utama

* Pesan **Welcome**, **Goodbye**, dan **Ban** dengan gambar & teks kustom.
* Sistem pemberian role melalui:

  * 🎮 Tombol (Button Role)
  * 📩 Dropdown (Select Menu Role)
  * 🔁 Emoji (Reaction Role)
* Pesan **Rules** yang dapat diatur dan dikirim otomatis.
* Fitur **Pengumuman** dari command admin.
* Sistem **Logging** aktivitas bot.
* Panel kontrol hanya untuk admin/staff via channel khusus.

---

🛠️ Perintah Bot

⚙️ Konfigurasi Channel

| Perintah                     | Deskripsi                                                |
| ---------------------------- | -------------------------------------------------------- |
| `^set_welcome <channel>`     | Mengatur channel untuk pesan welcome                     |
| `^set_goodbye <channel>`     | Mengatur channel untuk pesan goodbye                     |
| `^set_ban <channel>`         | Mengatur channel untuk pesan ban                         |
| `^set_announce <channel>`    | Mengatur channel pengumuman                              |
| `^set_control <channel>`     | Mengatur channel kontrol admin/staff                     |
| `^set_role <channel>`        | Mengatur channel untuk role (tombol, reaction, dropdown) |
| `^verif_role <channel>`      | Mengatur channel verifikasi                              |
| `^set_log_channel <channel>` | Mengatur channel logging aktivitas bot                   |

---

👋 Welcome, Goodbye, dan Ban Message

| Perintah        | Deskripsi               |
| --------------- | ----------------------- |
| `^test_welcome` | Kirim pesan uji welcome |
| `^test_goodbye` | Kirim pesan uji goodbye |
| `^test_ban`     | Kirim pesan uji ban     |

---

📜 Rules

| Perintah                       | Deskripsi                                       |
| ------------------------------ | ----------------------------------------------- |
| `^set_rules <pesan>`           | Mengatur isi rules                              |
| `^set_rules_channel <channel>` | Mengatur channel untuk rules                    |
| `^send_rules`                  | Mengirim rules ke channel yang sudah ditentukan |

---

📢 Pengumuman

| Perintah            | Deskripsi |                                                 |
| ------------------- | --------- | ----------------------------------------------- |
| \`^announce <judul> | <pesan>\` | Mengirim pengumuman dengan format judul dan isi |

---

🎮 Button Role

| Perintah                                       | Deskripsi                                                     |
| ---------------------------------------------- | ------------------------------------------------------------- |
| `^add_button_role <label> <warna> <nama_role>` | Menambahkan tombol untuk pemberian role ke channel verifikasi |

---

🔁 Reaction Role

| Perintah                                      | Deskripsi              |                                                            |
| --------------------------------------------- | ---------------------- | ---------------------------------------------------------- |
| \`^add\_reaction\_roles \<emoji1, Nama Role 1 | emoji2, Nama Role 2>\` | Menambahkan reaksi ke pesan untuk memberikan role otomatis |

---

📩 Dropdown Role

| Perintah                                   | Deskripsi                                   |
| ------------------------------------------ | ------------------------------------------- |
| `^add_dropdown_role <role1, role2, role3>` | Menambahkan dropdown untuk memilih role     |
| `^remove_dropdown_role <message_id>`       | Menghapus dropdown role dari pesan tertentu |

| Command        | Akses Dibutuhkan                                  |
| -------------- | ------------------------------------------------- |
| Semua `^set_*` | Admin (punya izin `Manage Server`)                |
| `^test_*`      | Admin                                             |
| `^announce`    | Admin dan harus dijalankan di channel kontrol     |
| `^set_roles`   | Admin atau Staff (berdasarkan role ID dalam kode) |

Harus menggunakan hosting seperti (Replit, Railway, dsb)

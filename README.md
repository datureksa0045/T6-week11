NAMA     : Datu Reksa hamza Putra
NIM      : F1D02310045

# Post Manager Desktop Application

Aplikasi desktop untuk mengelola data post menggunakan API nyata dengan Python dan PySide6. Aplikasi ini mendukung operasi CRUD lengkap dengan UI yang responsif dan threading untuk mencegah UI freeze.

## Fitur

**Tampilkan Daftar Posts** - Ambil semua posts via GET, tampilkan dalam tabel dengan kolom: ID, Title, Author, Status

**Detail Post** - Klik baris tabel untuk menampilkan detail lengkap post (title, body, author, slug, status, comments) di panel samping

**Tambah Post** - Form input untuk POST post baru (title, body, author, slug, status), tampilkan ID yang dikembalikan server

**Edit Post** - Pilih post dari tabel, ubah data via PUT, tampilkan konfirmasi sukses

**Hapus Post** - Pilih post dari tabel, hapus via DELETE dengan konfirmasi dialog terlebih dahulu (cascade delete — semua comments ikut terhapus)

**Threading** - Semua API call berjalan di thread terpisah, UI tidak akan freeze

**State Handling** - Menampilkan status loading saat request berjalan, pesan error jika gagal

## Screenshot
1. [Tampilan Awal] <img width="1531" height="986" alt="Tampilan Awal" src="https://github.com/user-attachments/assets/b8b476d9-3393-41cd-903d-76ad067fe63e" />
2. [Add Post] <img width="797" height="690" alt="Add Post" src="https://github.com/user-attachments/assets/a0d746ac-1e46-44c6-84d0-520e82dea670" />
3. [Hasil Add] <img width="1544" height="978" alt="Hasil Add" src="https://github.com/user-attachments/assets/e838f1b4-6aa0-430e-a4f0-7b4fe9bac4dd" />
4. [Edit Post] <img width="802" height="690" alt="Edit Post" src="https://github.com/user-attachments/assets/a22857c4-083c-4122-8f2b-03fc2cbbdc92" />
5. [Hasil Edit] <img width="1544" height="981" alt="Hasil Edit" src="https://github.com/user-attachments/assets/8e9e3d50-3769-4476-9326-41b523d43178" />
6. [Delete confirm] <img width="431" height="184" alt="Del Conf" src="https://github.com/user-attachments/assets/01c68d3b-a2cc-4e6c-b0e0-5e64ce1e628a" />
7. [Delete Success] <img width="275" height="170" alt="Del succ" src="https://github.com/user-attachments/assets/2e6b701e-15e4-42b6-a71b-f886fae16327" />




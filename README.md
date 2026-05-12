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
1. Screenshot\Tampilan Awal.png
2. Screenshot\Add Post.png
3. Screenshot\Hasil Add.png
4. Screenshot\Edit Post.png
5. Screenshot\Hasil Edit.png
6. Delete Screenshot\Del Conf.png  Screenshot\Del succ.png
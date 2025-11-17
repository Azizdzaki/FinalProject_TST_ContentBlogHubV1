# II3160 - Final Project: Content Blog Hub (Milestone 4)

Repositori ini berisi pengerjaan Final Project untuk mata kuliah **II3160 Teknologi Sistem Terintegrasi**.

* **Mahasiswa:** Muhammad Azizdzaki Khrisnanurmuflih (18223128)
* **Domain:** Sistem Blog
* **Layanan:** Layanan Optimasi Penemuan Konten Pada Sistem Blog
* [cite_start]**Deliverable Saat Ini:** **Tahap 4 - Implementasi Awal** [cite: 16]

## 🚀 Gambaran Umum

[cite_start]Tujuan dari *milestone* ini adalah menerjemahkan **Tahapan Desain Taktis (Deliverable 3)** [cite: 4450-4640] [cite_start]menjadi kode API dasar yang fungsional menggunakan FastAPI[cite: 16, 29].

### Bounded Context yang Diimplementasikan

[cite_start]Implementasi ini berfokus secara eksklusif pada **`Content Discovery Context` (BC2)** [cite: 4522-4524, 4549].

[cite_start]Konteks ini bertanggung jawab untuk mengimplementasikan **Core Domain** [cite: 4481-4483][cite_start], yaitu logika `Filter dan Pencarian Berbasis Tag atau Kategori`[cite: 4482]. [cite_start]API ini menerima kriteria pencarian dari pengguna dan mengembalikan daftar artikel yang relevan[cite: 4477].

Untuk tujuan pengujian, data dari `Content Catalog Context` (BC1) disimulasikan sebagai *mock database* (data *in-memory*).

## ⚙️ Teknologi yang Digunakan

* **Python 3.10+**
* [cite_start]**FastAPI**: *Framework* untuk membangun API [cite: 29, 2406-2407].
* [cite_start]**Uvicorn**: Server ASGI untuk menjalankan FastAPI [cite: 2404-2405].
* [cite_start]**Pydantic**: Untuk validasi dan pemodelan data [cite: 2421, 2577-2582].

## 📚 Struktur Proyek

[cite_start]Struktur direktori ini didasarkan pada materi kuliah `Application-Structure` [cite: 2949-2959] untuk memastikan modularitas.
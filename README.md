# Content Blog Hub

Content Blog Hub adalah sebuah layanan *backend* (API) yang dirancang untuk **Layanan Optimasi Penemuan Konten Pada Sistem Blog**. Dibuat dengan **Python**, **FastAPI**, dan **Pydantic**, dan berfokus pada implementasi *Core Domain* (Content Discovery Context) dari desain DDD.

## Cara Memulai Pengembangan

Untuk mengerjakan proyek ini di komputer Anda pengembangan lokal ikuti langkah-langkah di bawah ini.

### Syarat

Pastikan Anda sudah menginstal **Python 3.9** atau lebih tinggi dan **Git**. Anda juga disarankan untuk familiar dengan *virtual environment* Python.

### Langkah Instalasi

1.  **Clone repositori ini :**
    ```bash
    git clone https://github.com/Azizdzaki/FinalProject_TST_ContentBlogHubV1.git
    ```

2.  **Masuk ke direktori proyek :**
    ```bash
    cd FinalProject_TST_ContentBlogHubV1
    ```

3.  **Buat dan aktifkan virtual environment :**
    ```bash
    # Buat venv
    python -m venv venv
    
    # Aktifkan di Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    
    # Aktifkan di macOS/Linux
    # source venv/bin/activate
    ```

4.  **Install semua dependensi yang dibutuhkan :**
    ```bash
    pip install -r requirements.txt
    ```

### Cara Menjalankan Sistem

1.  **Jalankan server pengembangan :**
    ```bash
    uvicorn app.main:app --reload atau Anda juga bisa menjalankan python app/main.py
    ```

2.  Setelah itu buka browser dan akses alamat server lokal yang muncul di terminal Anda biasanya http://localhost:8000/docs. Aplikasi akan otomatis me-reload setiap kali Anda menyimpan perubahan pada kode.

### Terima Kasih!
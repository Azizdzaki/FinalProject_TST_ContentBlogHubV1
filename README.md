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
    python -m uvicorn main:app --reload
    ```

2.  Setelah itu buka browser dan akses alamat server lokal yang muncul di terminal Anda biasanya http://127.0.0.1:8000/docs. Aplikasi akan otomatis me-reload setiap kali Anda menyimpan perubahan pada kode.

## Pengujian & CI/CD

### Menjalankan Unit Test Lokal

Proyek ini menggunakan **pytest** dengan target coverage **>95%**.

**Cara menjalankan test dari terminal di root project folder:**

```bash
# 1. Pastikan Anda di folder root project (bukan di folder tests/)
cd C:\Coding\Github\FinalProject_TST_ContentBlogHubV1

# 2. Jalankan semua test
pytest

# 3. Jalankan test dengan coverage report
pytest --cov=. --cov-report=term-missing

# 4. Jalankan test dan enforce coverage minimum 95%
pytest --cov=. --cov-fail-under=95

# 5. Jalankan test spesifik
pytest tests/test_auth.py -v
pytest tests/test_discovery.py::TestDiscoveryFilterCategory -v

# 6. Jalankan dengan output verbose
pytest -v

# 7. Jalankan dengan last failed test
pytest --lf
```

**PENTING: Jalankan dari root folder project, BUKAN dari folder `tests/`**

### Struktur Test

```
tests/
├── conftest.py              # Pytest fixtures (client, token, auth_headers)
├── test_auth.py             # 13 test cases untuk authentication
└── test_discovery.py        # 30+ test cases untuk discovery endpoint
```

### Test Coverage Details

**test_auth.py (13 test cases):**
- Login berhasil dengan user 1 & user 2
- Login gagal (password salah & username tidak ada)
- Empty credentials
- Verify password (correct, incorrect, case-sensitive)
- Create access token (valid, without expiry, different data)
- Root endpoint test

**test_discovery.py (30+ test cases):**
- Filter kategori (Tutorial, Berita Teknologi, non-existent, case-insensitive)
- Filter tags (single, multiple, non-existent, case-insensitive)
- Kombinasi kategori + tags
- Pagination (limit 1, 2, 10)
- Empty results
- Security tests (no token, invalid token, malformed header, empty token)
- Edge cases

### Contoh Output Test

```bash
$ pytest --cov=. --cov-fail-under=95

=================== test session starts ====================
collected 43 items

tests/test_auth.py::TestAuthenticationLogin::test_login_success PASSED
tests/test_auth.py::TestAuthenticationLogin::test_login_wrong_password PASSED
tests/test_discovery.py::TestDiscoveryFilterCategory::test_filter_category_tutorial PASSED
...

===================== 43 passed in 1.24s ===================
Name           Stmts   Miss  Cover   Missing
auth/security.py      35     0    100%
routes/discovery.py   25     0    100%
routes/auth.py        20     0    100%
models/user.py        12     0    100%
...
TOTAL             180     2     99%

coverage PASSED (>95%)
```

### GitHub Actions CI/CD

Pipeline otomatis berjalan setiap kali Anda push ke branch `main`:

1. **Setup Environment** - Setup Python 3.9, 3.10, 3.11
2. **Install Dependencies** - Install dari requirements.txt
3. **Linting** - Check code quality dengan flake8
4. **Run Tests** - Jalankan pytest dengan enforcement coverage ≥95%
5. **Upload Coverage** - Upload ke Codecov

**Workflow akan FAIL jika:**
- Ada syntax errors atau undefined names
- Coverage < 95%
- Test case gagal

Cek status di GitHub Actions tab di repository.

### Terima Kasih!
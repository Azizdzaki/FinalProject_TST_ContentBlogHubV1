from fastapi import FastAPI
from routes.discovery import discovery_router
from routes.auth import router as auth_router  # Import auth router


# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Content Blog Hub API",
    description="API untuk Optimasi Penemuan Konten Pada Sistem Blog.",
    version="0.2.0"  # Naikkan versi
)

# Daftarkan Router
app.include_router(auth_router)       # Router Login (/token)
app.include_router(  # Router Discovery (/discovery) - Terproteksi
    discovery_router
)


@app.get("/", tags=["Root"])
async def read_root():
    msg = "Selamat datang di Content Blog Hub API (Authenticated)."
    return {"message": msg}

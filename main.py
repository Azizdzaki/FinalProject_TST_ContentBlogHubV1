from fastapi import FastAPI
import uvicorn
from routes.discovery import discovery_router

app = FastAPI(
    title="Content Blog Hub API",
    description="API untuk Layanan Optimasi Penemuan Konten Pada Sistem Blog.",
    version="0.1.0"
)

app.include_router(discovery_router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Selamat datang di Content Blog Hub API."}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",       
        host="127.0.0.1",  
        port=8000,         
        reload=True        
    )
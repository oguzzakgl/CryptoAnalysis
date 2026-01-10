# 1. IMPORTLAR
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import services # Yazdığımız services.py dosyasını import ediyoruz

# 2. UYGULAMAYI BASLATIN
app = FastAPI()

# 3. STATIK DOSYALARI TANITIN 
# (Henüz static klasörüne bir şey koymadık ama kalsın)
app.mount("/static", StaticFiles(directory="Portfolio/04_Crypto_Analysis/static"), name="static")

# 4. SABLONLARI (HTML) TANITIN
# templates klasörünün tam yolunu veriyoruz
templates = Jinja2Templates(directory="Portfolio/04_Crypto_Analysis/templates")

# 5. ANA SAYFA ENDPOINTI (GET /)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # index.html dosyasını ekrana bas
    return templates.TemplateResponse("index.html", {"request": request})

# 6. API ENDPOINTI
@app.get("/api/analyze/{coin_id}")
async def analyze_coin(coin_id: str):
    # services.py'deki fonksiyonu çağırıp sonucu döndür
    return services.get_crypto_data(coin_id)

# 7. SUNUCUYU CALISTIRMA KODU
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
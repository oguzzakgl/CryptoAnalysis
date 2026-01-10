import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

# Statik klasör kontrolü (Eğer yoksa oluştur)
STATIC_DIR = "Portfolio/04_Crypto_Analysis/static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

def get_crypto_data(coin_id="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        prices = data.get("prices", [])
        
        # DataFrame oluştur
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        
        # Tarihi düzenle
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        
        # --- MATPLOTLIB İLE GRAFİK ÇİZİMİ ---
        plt.figure(figsize=(10, 5)) # Grafik boyutu (10x5 inç)
        plt.plot(df["date"], df["price"], label=f"{coin_id.title()} Fiyatı", color="blue", linewidth=2)
        
        plt.title(f"{coin_id.title()} - Son {days} Günlük Değişim")
        plt.xlabel("Tarih")
        plt.ylabel("Fiyat ($)")
        plt.grid(True, linestyle="--", alpha=0.7) # Izgaraları aç
        plt.legend()
        
        # Grafiği Kaydet (Web sitesinin görebileceği yere)
        filename = f"{coin_id}.png"
        save_path = os.path.join(STATIC_DIR, filename)
        
        # Eğer eski grafik varsa silmeliyiz (üstüne yazsın)
        if os.path.exists(save_path):
            os.remove(save_path)
            
        plt.savefig(save_path)
        plt.close() # Hafızayı temizle (önemli!)
        
        # ------------------------------------
        
        # İstatistikler
        current = df["price"].iloc[-1]
        mean = df["price"].mean()
        mx = df["price"].max()
        mn = df["price"].min()
        
        return {
            "coin": coin_id,
            "current_price": round(current, 2),
            "mean_price": round(mean, 2),
            "max_price": round(mx, 2),
            "min_price": round(mn, 2),
            # Grafik verisi yerine artık RESİM ADRESİ dönüyoruz
            "chart_url": f"/static/{filename}"
        }

    except Exception as e:
        print(f"HATA: {e}")
        return {}
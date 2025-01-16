from typing import Union
import requests
from lxml import html
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por la URL específica de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#url con precios actuales de los cedears sacada de IOL (Invertir Online)
urls_cedears = ['https://iol.invertironline.com/titulo/cotizacion/BCBA/AL30D/BONO-REP.-ARGENTINA-USD-STEP-UP-2030/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/SPYD/ETF-SPDR-S-P-500/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/EEMD/ETF-ISHARES-MSCI-EMERGING-MARKET',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/MELID/MERCADOLIBRE/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/BABAD/ALIBABA-GROUP/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/NKED/NIKE/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/MCDD/MCDONALD-S/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/AMZND/AMAZON/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/GGAL/GRUPO-FINANCIERO-GALICIA-S.A/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/IWMD/ETF-ISHARES-TRUST-RUSSELL-2000/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/BRKBD/BERKSHIRE-HATHAWAY/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/MRCLO/ON-GEMSA-CTR-CLASE-XX-VTO.-27-07-2025/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/NIOD/NIO-INC./',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/VD/VISA/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/VISTD/VISTA-ENERGY-S.A.B.-DE-C.V./',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/ABNBD/AIRBNB--INC./',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/TCOM/TRIP.COM-GROUP/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/JDD/JD.COM/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/UBERD/UBER-TECHNOLOGIES--INC./',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/GOGLD/GOOGLE/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/MSFTD/MICROSOFT/',
'https://iol.invertironline.com/titulo/cotizacion/BCBA/METAD/META-PLATFORMS-INC/',


 ]
names_cedears = ['AL30', 'SPY', 'EEM', 'MELI', 'BABA', 'NKE', 'MCD', 'AMZN','GGAL','IWM', 'BRKB', 'MRCLO', 'NIO', 'V', 'VIST', 'ABNB', 'TCOM', 'JD', 'UBER', 'GOOGL', 'MSFT', 'META']

# Función para obtener el precio de la página
def get_price_from_page():
    try:
        resultado = []
        for name, url in zip(names_cedears, urls_cedears):
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                ultimo_precio = soup.find("span", {"data-field": "UltimoPrecio"})
                if ultimo_precio:
                    resultado.append({name: ultimo_precio.text.strip()})
                else:
                    print("No se encontró el campo 'UltimoPrecio'.")
            else:
                print(f"Error al acceder a la página: {response.status_code}")
        return resultado
    except Exception as e:
        print(f"Se produjo un error: {e}")

@app.get("/api/cotizaciones/cedears")
def read_root():
    quotes = get_price_from_page()
    return quotes


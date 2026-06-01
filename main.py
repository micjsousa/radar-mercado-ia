import os
import requests
import feedparser
from deep_translator import GoogleTranslator

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

feeds = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EBVSP,BRL%3DX&region=US&lang=en-US",

    "https://feeds.reuters.com/reuters/businessNews",

    "https://feeds.reuters.com/reuters/worldNews",

    "https://feeds.reuters.com/news/wealth",

    "https://www.cnbc.com/id/100003114/device/rss/rss.html"
]

for feed in feeds:

    rss = feedparser.parse(feed)

    if not rss.entries:
        continue



    noticia = rss.entries[0]
    titulo = noticia.title
resumo = getattr(noticia, "summary", "")
try:
    titulo_pt = GoogleTranslator(
        source='auto',
        target='pt'
    ).translate(titulo)
except:
    titulo_pt = titulo

try:
    resumo_pt = GoogleTranslator(
        source='auto',
        target='pt'
    ).translate(resumo[:400])
except:
    resumo_pt = resumo[:400]
    
link_atual = noticia.link

try:
    with open("ultima_noticia.txt", "r") as f:
        ultima = f.read().strip()
except:
    ultima = ""

if titulo == ultima:
    exit()

with open("ultima_noticia.txt", "w") as f:
    f.write(titulo)

    texto = (titulo + " " + resumo).lower()

    categoria = "Mercado"
    urgencia = "🟢 BAIXA"
    win = "🟡 NEUTRO"
    wdo = "🟡 NEUTRO"
    autoridade = "Não identificada"

    # AUTORIDADES

    if "trump" in texto:
        autoridade = "🇺🇸 Donald Trump"

    elif "powell" in texto:
        autoridade = "🇺🇸 Jerome Powell"

    elif "lula" in texto:
        autoridade = "🇧🇷 Lula"

    elif "haddad" in texto:
        autoridade = "🇧🇷 Fernando Haddad"

    elif "galipolo" in texto:
        autoridade = "🇧🇷 Gabriel Galípolo"

    elif "xi" in texto:
        autoridade = "🇨🇳 Xi Jinping"

    elif "putin" in texto:
        autoridade = "🇷🇺 Vladimir Putin"

    # GEOPOLÍTICA

    geopolitica = [
        "war",
        "iran",
        "israel",
        "ukraine",
        "russia",
        "china",
        "tariff",
        "sanction",
        "conflict"
    ]

    if any(p in texto for p in geopolitica):

        categoria = "🌎 GEOPOLÍTICA"
        urgencia = "🔴 ALTA"

        win = "🔴 BAIXISTA"
        wdo = "🟢 ALTISTA"

    # JUROS

    juros = [
        "fed",
        "interest rate",
        "powell",
        "inflation",
        "central bank",
        "copom",
        "selic"
    ]

    if any(p in texto for p in juros):

        categoria = "🏦 JUROS"

        win = "🟠 MÉDIO IMPACTO"
        wdo = "🟠 MÉDIO IMPACTO"

    # COMMODITIES

    commodities = [
        "oil",
        "coffee",
        "soybean",
        "corn",
        "gold"
    ]

    if any(p in texto for p in commodities):

        categoria = "🛢 COMMODITIES"

        win = "🟠 MÉDIO/ALTO IMPACTO"
        wdo = "🟠 MÉDIO/ALTO IMPACTO"

    mensagem = f"""
📢 RADAR MERCADO IA

🏷 Categoria:
{categoria}

👤 Autoridade:
{autoridade}

📰 Título:
{titulo}

📄 Resumo:
{resumo[:400]}

📊 WIN:
{win}

💵 WDO:
{wdo}

🔥 Urgência:
{urgencia}

🔗 Link:
{noticia.link}

🤖 Radar automático
"""

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mensagem
        }
    )

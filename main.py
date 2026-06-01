import os
import requests
import feedparser

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

rss = feedparser.parse(
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EBVSP,BRL%3DX&region=US&lang=en-US"
)

if rss.entries:

    noticia = rss.entries[0]
    
link_atual = noticia.link

try:
    with open("ultima_noticia.txt", "r") as f:
        ultimo_link = f.read().strip()
except:
    ultimo_link = ""

if link_atual == ultimo_link:
    print("Notícia repetida")
    exit()

with open("ultima_noticia.txt", "w") as f:
    f.write(link_atual)
    titulo = noticia.title
    resumo = getattr(noticia, "summary", "")

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

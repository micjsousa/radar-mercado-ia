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

    resumo = getattr(noticia, "summary", "Resumo não disponível")

    mensagem = f"""
📢 RADAR MERCADO IA

📰 Título:
{noticia.title}

📄 Resumo:
{resumo[:300]}

🎯 Impacto:
Em análise

🔗 Link:
{noticia.link}

🤖 Enviado automaticamente
"""

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mensagem
        }
    )

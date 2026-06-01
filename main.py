import os
import requests
import feedparser

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

rss = feedparser.parse(
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EBVSP,BRL%3DX&region=US&lang=en-US"
)

PALAVRAS_IMPORTANTES = [
    "fed", "powell", "cpi", "inflation", "payroll",
    "pce", "interest rate", "treasury", "bond",
    "oil", "opec", "iran", "israel", "china",
    "trump", "tariff", "war", "recession",
    "brazil", "ibovespa", "real", "dollar",
    "fiscal", "tax", "central bank"
]

if rss.entries:

    noticia = rss.entries[0]

    titulo = noticia.title
    resumo = getattr(noticia, "summary", "")

    texto_completo = (titulo + " " + resumo).lower()

    relevante = any(
        palavra in texto_completo
        for palavra in PALAVRAS_IMPORTANTES
    )

    if relevante:

        impacto_win = "⚪ Em análise"
        impacto_wdo = "⚪ Em análise"

        if any(x in texto_completo for x in ["fed", "powell", "cpi", "payroll", "pce"]):
            impacto_wdo = "🔴 ALTO IMPACTO"

        if any(x in texto_completo for x in ["war", "iran", "israel", "oil", "opec"]):
            impacto_win = "🟠 MÉDIO/ALTO IMPACTO"
            impacto_wdo = "🟠 MÉDIO/ALTO IMPACTO"

        mensagem = f"""
📢 RADAR MERCADO IA

📰 {titulo}

📄 Resumo:
{resumo[:400]}

📊 WIN:
{impacto_win}

💵 WDO:
{impacto_wdo}

🔗 {noticia.link}

🤖 Radar automático
"""

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": mensagem
            }
        )

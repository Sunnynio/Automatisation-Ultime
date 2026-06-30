import os

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_DIGEST_DATABASE_ID = os.getenv("NOTION_DIGEST_DATABASE_ID")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Bangkok")


def get_notion_client() -> Client:
    if not NOTION_TOKEN:
        raise ValueError(
            "NOTION_TOKEN manquant. Créez un fichier .env avec :\n"
            "  NOTION_TOKEN=secret_votreclé\n"
            "Voir .env.example pour le template complet."
        )
    return Client(auth=NOTION_TOKEN)

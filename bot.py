import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus .env
load_dotenv()

# Bot Token aus der Umgebungsvariablen
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot Client erstellen
intents = discord.Intents.default()
intents.message_content = True  # Berechtigung für das Lesen von Nachrichten

client = discord.Client(intents=intents)

# Funktion zum Überprüfen von Vinted-Artikeln
def check_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrahiere Titel und Preis des Artikels
        title = soup.find('h1', {'class': 'item-title'}).get_text(strip=True)
        price = soup.find('span', {'class': 'item-price'}).get_text(strip=True)

        # Überprüfe auf verdächtige Artikel
        if 'fake' in title.lower() or 'unrealistisch' in price:
            return f"Der Artikel {title} könnte gefälscht sein. Preis: {price}"
        else:
            return f"Der Artikel {title} scheint echt zu sein. Preis: {price}"
    except Exception as e:
        return f"Fehler beim Abrufen des Artikels: {str(e)}"

# Event, wenn der Bot bereit ist
@client.event
async def on_ready():
    print(f'Bot ist eingeloggt als {client.user}')

# Event, wenn eine Nachricht gesendet wird
@client.event
async def on_message(message):
    # Verhindere, dass der Bot auf sich selbst reagiert
    if message.author == client.user:
        return

    # Befehl zum Überprüfen von Vinted-Artikeln nur für bestimmte Rollen
    if message.content.startswith("!check"):
        role_name = "Verifizierte Rolle"  # Hier den Namen der Rolle eintragen
        if any(role.name == role_name for role in message.author.roles):
            url = message.content.split(" ")[1]  # URL extrahieren
            result = check_article(url)  # Artikel prüfen
            await message.channel.send(result)  # Ergebnis zurücksenden
        else:
            await message.channel.send("Du hast nicht die erforderliche Rolle, um diesen Befehl zu verwenden.")

# Starte den Bot
client.run(TOKEN)

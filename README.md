# Mega Telegram Bot fuer TikTok-Profile

Dieser Bot ist fuer Anfaenger gedacht.

## Was er kann
- /user <username> zeigt Profilinfos
- /save <username> speichert einen Snapshot lokal
- /history <username> zeigt bekannte Aenderungen
- /note <username> <text> speichert eine Notiz
- /seen <username> zeigt, ob du das Profil schon kennst
- /help zeigt Hilfe

## Wichtige Grenze
Der Bot kann nur das speichern und vergleichen, was deine ScrapTik-Abfrage liefert.
Wenn ein Profil noch nie gespeichert wurde, gibt es dafuer auch noch keine eigene Historie.

## Start auf dem Mac
1. Terminal oeffnen
2. In den Ordner gehen
3. Pakete installieren:
   pip3 install -r requirements.txt
4. .env.example in .env kopieren
5. In .env deine echten Werte einsetzen
6. Bot starten:
   python3 bot.py

## So findest du die zwei ScrapTik-Werte
- RAPIDAPI_HOST
- SCRAPTIK_USER_ENDPOINT

Gehe in RapidAPI auf dein ScrapTik-Abo, dann:
- Endpoints
- User Info oder User Details oeffnen
- Code Snippet auf Python/Requests stellen
- dort Host und URL herauskopieren

## Beispiele in Telegram
- /user tiktok
- /save tiktok
- /history tiktok
- /note tiktok Schon mal gesehen im April
- /seen tiktok

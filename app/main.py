import json

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.config import TELEGRAM_BOT_TOKEN
from app.formatters import format_full_report, format_seen
from app.services.normalize import normalize_user_payload
from app.services.scraptik_client import ScrapTikError, fetch_user
from app.storage import add_note, upsert_profile


async def run_lookup_and_save(update: Update, username: str):
    try:
        payload = fetch_user(username)

        with open("debug_payload.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        normalized = normalize_user_payload(payload)
        profile = upsert_profile(username, payload, normalized)
        text = format_full_report(profile)
        await update.message.reply_text(text)

    except ScrapTikError as e:
        await update.message.reply_text(f"ScrapTik Fehler: {e}")
    except Exception as e:
        await update.message.reply_text(f"Allgemeiner Fehler: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        username = context.args[0].replace("@", "").strip()
        await run_lookup_and_save(update, username)
        return

    text = (
        "Hallo! Ich bin dein TikTok Bot.\n\n"
        "Benutze:\n"
        "/user username\n\n"
        "Beispiel:\n"
        "/user tiktok"
    )
    await update.message.reply_text(text)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Bitte so schreiben: /user username")
        return

    username = context.args[0].replace("@", "").strip()
    await run_lookup_and_save(update, username)


async def note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Bitte so schreiben: /note username dein text")
        return

    username = context.args[0].replace("@", "").strip()
    note_text = " ".join(context.args[1:]).strip()
    profile = add_note(username, note_text)
    await update.message.reply_text("Notiz gespeichert.\n\n" + format_seen(profile))


def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Fehler: TELEGRAM_BOT_TOKEN fehlt in deiner .env Datei.")
        return

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("user", user_cmd))
    app.add_handler(CommandHandler("note", note_cmd))

    print("Bot laeuft ...")
    app.run_polling()


if __name__ == "__main__":
    main()
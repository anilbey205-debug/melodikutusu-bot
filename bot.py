from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes
import yt_dlp
from uuid import uuid4

TOKEN = "8001194820:AAHxqz2H7niXknI5y2es-bYnCa6G20WLm9I"

ydl_opts = {"quiet": True, "default_search": "ytsearch", "noplaylist": True}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Merhaba! Ben Melodi Kutususu'yum 🎶\n\n"
        "Herhangi sohbette şöyle kullanabilirsin:\n"
        "@MelodiKutusuBot   şarkı adı\n\n"
        "Örnek: @MelodiKutusuBot   tarkan şımarık\n\n"
        "Türkçe komut: /ara şarkı adı (arama yapar)\n"
        "İyi eğlenceler! 🔥",
        parse_mode=ParseMode.MARKDOWN
    )

async def ara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Kullanım: /ara tarkan şımarık")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch5:{query}", download=False)["entries"] or []

    if not results:
        await update.message.reply_text("Şarkı bulunamadı 😔")
        return

    text = "Bulunan sonuçlar:\n\n"
    for i, v in enumerate(results, 1):
        title = v.get("title", "Başlık yok")
        url = v.get("webpage_url", "")
        dur = v.get("duration", 0)
        dur_str = f"{dur//60:02d}:{dur%60:02d}" if dur else "??:??"
        text += f"{i}. {title} ({dur_str})\n{url}\n\n"

    await update.message.reply_text(text)

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        await update.inline_query.answer([])
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch5:{query}", download=False)["entries"] or []

    inline_results = []
    for v in results:
        title = v.get("title", "Başlık yok")
        url = v.get("webpage_url", "")
        dur = v.get("duration", 0)
        dur_str = f"{dur//60:02d}:{dur%60:02d}" if dur else "??:??"
        inline_results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=title,
                description=f"🎵 {dur_str}",
                thumb_url=v.get("thumbnail"),
                input_message_content=InputTextMessageContent(f"**{title}**\nSüre: {dur_str}\n{url}", parse_mode=ParseMode.MARKDOWN)
            )
        )

    await update.inline_query.answer(inline_results, cache_time=5)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ara", ara))
app.add_handler(InlineQueryHandler(inline_query))

print("BOT ÇALIŞIYOR!")
app.run_polling()

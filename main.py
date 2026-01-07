from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

# ======= تنظیمات =======
TELEGRAM_TOKEN = "8569288881:AAG5KM76e5jw9iSkL_zaym_94Z97u4_fB3o"
STEAM_API_KEY = "HUIU75Y04Z5IVHEW"

# ======= تابع استارت =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ایتم‌ها", callback_data="items_list")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! به ربات Dota 2 خوش آمدید.", reply_markup=reply_markup)

# ======= گرفتن لیست آیتم‌ها =======
def get_dota2_items():
    url = f"https://api.steamwebapi.com/v1/market/items?game_id=570&key={STEAM_API_KEY}"
    res = requests.get(url).json()

    # بررسی اینکه data و items وجود داشته باشند
    if "data" in res and "items" in res["data"]:
        return res["data"]["items"]
    else:
        print("Error: 'items' not found in API response")
        print(res)  # برای دیدن پاسخ واقعی API
        return []



# ======= گرفتن جزئیات آیتم =======
def get_item_details(item_id):
    url = f"https://api.steamwebapi.com/v1/market/item/{item_id}?key={STEAM_API_KEY}"
    res = requests.get(url).json()

    if "data" in res:
        return res["data"]
    else:
        print("Error: 'data' not found in API response")
        print(res)  # بررسی پاسخ واقعی
        return None


# ======= هندلر دکمه‌ها =======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "items_list":
        items = get_dota2_items()
        keyboard = []
        for item in items[:20]:  # فقط 20 آیتم اول
            keyboard.append([InlineKeyboardButton(item["name"], callback_data=f"item_{item['id']}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("لیست آیتم‌ها:", reply_markup=reply_markup)

    elif query.data.startswith("item_"):
        item_id = query.data.replace("item_", "")
        item = get_item_details(item_id)
        if item:
            msg = f"🔹 {item['name']}\n"
            msg += f"💰 قیمت متوسط: {item['price']['average']}\n"
            msg += f"📊 Lowest: {item['price']['lowest']}\n"
            msg += f"🎮 Game: Dota 2\n"
            msg += f"⭐ Rarity: {item.get('rarity', 'نامعلوم')}\n"
            msg += f"🧩 Type: {item.get('type', 'نامعلوم')}\n"
            await query.message.reply_photo(photo=item['image'], caption=msg)
        else:
            await query.message.reply_text("مشخصات آیتم پیدا نشد!")

# ======= راه‌اندازی ربات =======
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")
app.run_polling()

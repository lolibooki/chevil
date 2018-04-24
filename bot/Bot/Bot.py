import telegram
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, RegexHandler, filters


TELEGRAM_TOKEN = "437283497:AAF_PIsNJe1AURGYKnKzHxjBKkMV7oYwOSo"
ITEM_LIST = [['http://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-11/256/honey-pot.png', 'عسل چرنوبیل قیمت 23432 تومان', 'add_chevil'],
             ['https://images.freshop.com/00073260000011/15d7f41f3e83d65cc0c087d2a0ed2d75_medium.png', 'عسل شاخ گوساله قیمت 23432 تومان', 'add_chorbil'],
             ['https://images.freshop.com/00011153146101/2ae35cb6bea7d5c5c957dc9341f45c2e_medium.png', 'عسل برگ استقدوس قیمت 23432 تومان', 'add_chibil']]
CART = "J:\\chevil\\bagghali\\bot\\Bot\\cart.json"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname) - %(message)s', level=logging.INFO)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("خرید", callback_data='1')],
                [InlineKeyboardButton("درباره ما", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('در صورتی که تمایل به خرید دارید دکمه /"خرید" و برای درباره ما /"درباره ما" رو فشار بدید', reply_markup= reply_markup)


def buttons(bot, update):  # TODO : add quality assurance here and in start()
    query = update.callback_query
    if query.data == '2':
        about_us(bot, update)
    elif query.data == '4':
        edit_card(bot, update)
    else:
        shop(bot, update)


def shop(bot, update):
    query = update.callback_query.data
    if query == '1':
        for item in ITEM_LIST:  # TODO : show from database
            keyboard = [[InlineKeyboardButton("اضافه به سبد", callback_data=item[2])]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_photo(photo=item[0],
                           chat_id=update.callback_query.message.chat_id,
                           caption=item[1],
                           reply_markup=reply_markup)
    if query[0:4] == 'add_':
        cart_file = open(CART, 'r+')
        with open(CART) as json_data:
            cart = json.load(json_data)
        if str(update.callback_query.message.chat_id) in cart['incomplete']:
            cart['incomplete'][str(update.callback_query.message.chat_id)]['cart'][query[4:]] = 1
        else:
            cart['incomplete'][str(update.callback_query.message.chat_id)] = {'cart': {query[4:]: 1}}
        cart_file.flush()
        cart_file.write(json.dumps(cart))
        cart_file.close()
        keyboard = [[InlineKeyboardButton("ادامه خرید", callback_data='1'),
                     InlineKeyboardButton("نهایی کردن خرید", callback_data='3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(text='محصول مورد نظر به لیست خرید اضافه شد',
                         chat_id=update.callback_query.message.chat_id,
                         message_id=update.callback_query.message.message_id,
                         reply_markup=reply_markup)
    if query == '3':
        bot.send_message(text="لطفا مکان خودتون رو از طریق ارسال مکان تلگرام ارسال نمایید:",
                         chat_id=update.callback_query.message.chat_id,
                         message_id=update.callback_query.message.message_id,)


def edit_card(bot, update):
    pass


def get_address(bot, update):
    long = update.message.location.longitude
    lat = update.message.location.latitude
    cart_file = open(CART, 'r+')
    with open(CART) as json_data:
        cart = json.load(json_data)
    cart['incomplete'][update.message.chat_id]['location'] = {'longitude': long, 'latitude': lat}
    cart_file.flush()
    cart_file.write(json.dumps(cart))
    cart_file.close()
    bot.send_message(text="آدرس ثبت شد. لطفا شماره تلفن ثابت خود را با فرمت کدشهر-شماره تلفن وارد نمایید",
                     chat_id=update.message.chat_id,
                     message_id=update.message.message_id)


def get_phone(bot, update):
    s_phone = update.message.text
    cart_file = open(CART, 'r+')
    with open(CART) as json_data:
        cart = json.load(json_data)
    cart['incomplete'][update.message.chat_id]['s_phone'] = str(s_phone)
    cart_file.flush()
    cart_file.write(json.dumps(cart))
    cart_file.close()
    bot.send_message(text="شماره تلفن ثابت شما ثبت شد. لطفا شماره همراه خود را با فرمت پیش شماره-شماره تلفن وارد نمایید",
                     chat_id=update.message.chat_id,
                     message_id=update.message.message_id)


def get_mobile(bot, update):
    mobile = update.message.text
    cart_file = open(CART, 'r+')
    with open(CART) as json_data:
        cart = json.load(json_data)
    cart['incomplete'][update.message.chat_id]['mobile_phone'] = str(mobile)
    cart_file.flush()
    cart_file.write(json.dumps(cart))
    cart_file.close()
    bot.send_message(
        text="خرید شما با موفقیت ثبت شد! کارشناسان ما با شما تماس خواهند گرفت",
        chat_id=update.message.chat_id,
        message_id=update.message.message_id)


def about_us(bot, update):
    bot.send_message(text="اینجا درباره ماست!!",
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id)


def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(buttons))
    dp.add_handler(MessageHandler(filters.location, get_address))
    dp.add_handler(RegexHandler(r'^0(\d{2})-(\d{7})|(\d{8})$', get_phone))
    dp.add_handler(RegexHandler(r'^0(\d{3})-(\d{7})$', get_mobile))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
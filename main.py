from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from copy import deepcopy
import os

from PIL import Image
import numpy as np
from io import BytesIO
from urllib.parse import urljoin
from style_transfer import NST
from gan import GAN

from config import *

gan_vangogh = GAN("vangogh")  # GAN
gan_monet = GAN("monet")  # GAN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

photo_buffer = {}


class InfoAboutUser:
    def __init__(self, type):
        self.type = type
        self.content = None
        self.style = None


def tensor2img(tensor):
    output = np.rollaxis(tensor.cpu().detach().numpy()[0], 0, 3)
    output = Image.fromarray(np.uint8(output * 255))
    bio = BytesIO()
    bio.name = 'result.jpeg'
    output.save(bio, 'JPEG')
    bio.seek(0)

    return bio


def simple_style_transfer(content_img, style_img, *params):
    model = NST(content_img, style_img, *params) # создание простой NST модели
    output = model.transfer()
    return tensor2img(output)


start_kb = InlineKeyboardMarkup()
start_kb.add(InlineKeyboardButton('Перенос одного стиля (NST)',
                                  callback_data='NST'))
start_kb.add(InlineKeyboardButton('Стилизация под Ван Гога (GAN)',
                                  callback_data='vangogh'))
start_kb.add(InlineKeyboardButton('Стилизация под Моне (GAN)',
                                  callback_data='monet'))

cancel_kb = InlineKeyboardMarkup()
cancel_kb.add( InlineKeyboardButton('Отмена', callback_data='main_menu'))


# start
@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.send_message(message.chat.id,
                           f"Привет, {message.from_user.first_name}!\nЯ Style transfer бот. " +
                           "Я умею переносить стиль с одной картинки на другую. " +
                           "Вот что я могу:", reply_markup=start_kb)

    # to remove reply keyboard
    # await bot.send_message(message.chat.id, "text", reply_markup = reply_keyboard.ReplyKeyboardRemove())


# help
@dp.message_handler(commands=['help'])
async def send_help(message):
    await bot.send_message(message.chat.id,
                           "Вот что я могу:", reply_markup=start_kb)


# text error
@dp.message_handler(content_types=['text'])
async def get_text(message):
    await bot.send_message(message.chat.id,
                           "Я тебя не понимаю. Вот что я могу:", reply_markup=start_kb)


# main menu
@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def main_menu(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("Вот что я могу:")
    await callback_query.message.edit_reply_markup(reply_markup=start_kb)


@dp.callback_query_handler(lambda c: c.data == 'NST')
async def st_1_style(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("Пришлите мне картинку, к которой нужно применить стиль. " +
                                           "Настоятельно рекомендую для хорошего качества присылать изображение "
                                           "в виде документа.")

    photo_buffer[callback_query.from_user.id] = InfoAboutUser("NST")


@dp.callback_query_handler(lambda c: c.data == 'vangogh')
async def st_2_style(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("Пришлите мне фотографию, и я добавлю на нее стиль Ван Гога. " +
                                           "Для хорошего качества лучше  присылать изображение как документ."
                                           )

    photo_buffer[callback_query.from_user.id] = InfoAboutUser("vangogh")


@dp.callback_query_handler(lambda c: c.data == 'monet')
async def st_3_style(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("Пришлите мне фотографию, и я добавлю на нее стиль Моне. " +
                                           "Для хорошего качества лучше  присылать изображение как документ."
                                           )

    photo_buffer[callback_query.from_user.id] = InfoAboutUser("monet")


# getting image
@dp.message_handler(content_types=['photo', 'document'])
async def get_image(message):
    if not hasattr(photo_buffer[message.chat.id], 'type'):
        await bot.send_message(message.chat.id,
                               "Сначала выбери тип style transfer`a.", reply_markup=start_kb)
        return

    if message.content_type == 'photo':
        img = message.photo[-1]

    else:
        img = message.document
        if img.mime_type[:5] != 'image':
            await bot.send_message(message.chat.id,
                                   "Загрузи, пожалуйста, файл в формате изображения.",
                                   reply_markup=start_kb)
            return

    file_info = await bot.get_file(img.file_id)
    photo = await bot.download_file(file_info.file_path)

    if photo_buffer[message.chat.id].type == "NST":
        if not photo_buffer[message.chat.id].content:  # если была прислана картинка контента
            photo_buffer[message.chat.id].content = photo
            await bot.send_message(message.chat.id,
                                   "Отлично, пришлите картинку стиля, который будет применён. " +
                                   "Для лучшего качества изображения лучше загружать в виде документа.")
        else:  # если была прислана картинка стиля
            photo_buffer[message.chat.id].style = photo
            # simple style transfer
            await bot.send_message(message.chat.id, "Начинаю обрабатывать, ждите...")
            try:
                output = simple_style_transfer(photo_buffer[message.chat.id].content, photo_buffer[message.chat.id].style, *PARAMS)
                await bot.send_document(message.chat.id, deepcopy(output))
                await bot.send_photo(message.chat.id, output)

            except Exception as err:
                print(err)

            await bot.send_message(message.chat.id,
                                   "Что будем делать дальше?", reply_markup=start_kb)

            del photo_buffer[message.chat.id]

    else:
        photo_buffer[message.chat.id].content = photo
        # gan transfer
        await bot.send_message(message.chat.id, "Начинаю обрабатывать, ждите...")
        try:
            if photo_buffer[message.chat.id].type == "vangogh":  # если нужно применить стиль Ван Гога
                output = tensor2img(gan_vangogh.transfer(photo))
            else: # если нужно применить стиль картин Моне
                output = tensor2img(gan_monet.transfer(photo))
            await bot.send_document(message.chat.id, deepcopy(output))
            await bot.send_photo(message.chat.id, output)

        except Exception as err:
            print(err)

        await bot.send_message(message.chat.id,
                               "Что будем делать дальше?", reply_markup=start_kb)

        del photo_buffer[message.chat.id]


if __name__ == '__main__':
    if CONNECTION_TYPE == 'POLLING':
        executor.start_polling(dp, skip_updates=True)

    else:
        # webhook setting
        webhook_path = f'/webhook/{BOT_TOKEN}'
        webhook_url = urljoin(WEBHOOK_HOST, webhook_path)

        # webserver setting
        webapp_host = '127.0.0.1'
        webapp_port = int(os.environ.get('PORT', WEBAPP_PORT))

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=webhook_path,
            skip_updates=True,
            host=webapp_host,
            port=webapp_port)
    executor.start_polling(dp, skip_updates=True)
# Style transfer telegram bot
Данный бот для телеграма переносит стиль с одних фотографий на другие.

## Режимы работы бота

У бота есть 3 режима работы:
- Простой перенос стиля с одного изображения на другое (NST)
- Стилизация изображений под картины Ван Гога (GAN)
- Стилизация изображений под картины Моне (GAN)

### Простой перенос стиля с одного изображения на другое
В данном режиме бот переносит стиль с первого изображения на второе.
Данный режим использует технологию Neural style transfer.

Возможные результаты работы данного режима:

Изначальное изображение    |  Переносимый стиль        |  Итоговое изображение
:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/content1.jpg" height="250" width="250">  |  <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/style2.jpg" height="250" width="230">  |   <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/nst_1.jpg" height="250"  width="250">
<img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/content2.jpg" height="250" width="250">  |  <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/style1.jpg" height="250" width="230">  |   <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/nst_2.jpg" height="250"  width="250">




### Стилизация изображений под картины Ван Гога
В данном режиме бот перерисовывает данное ему изображение так, чтобы оно было похоже по стилю на картины Ван Гога. При этом бот  использует предобученную генеративную сеть(GAN) из  проекта: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.

Данный режим использует технологию GAN.

Возможные результаты работы данного режима бота:

Изначальное изображение    |  Итоговое изображение
:-------------------------:|:-------------------------:
<img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/plain1.jpg" height="250" width="375">  |  <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/plain1_transfered.jpg" height="250"  width="250">
<img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/plain2.jpg" height="250" width="378">  |  <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/plain2_transfered.jpg" height="250"  width="250">


### Стилизация изображений под картины Моне
В данном режиме бот перерисовывает данное ему изображение так, чтобы оно было похоже по стилю на картины Моне. При этом бот  использует предобученную генеративную сеть из этого проекта: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.

Данный режим использует технологию GAN.

  
Возможные результаты работы данного режима бота:

Изначальное изображение    |  Итоговое изображение
:-------------------------:|:-------------------------:
<img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/monet1.jpg" height="250" width="375">  |  <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/monet1_transfered.jpg" height="250"  width="250">
<img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/monet2.jpg" height="250" width="378">  |  <img src="https://github.com/Mattew017/StyleTransferBot/blob/main/images/monet2_transfered.jpg" height="250"  width="250">

## Информация по запуску бота
Для запуска  бота у себя необходимо добавить в файл `config.py` следующие данные:

- `<BOT_TOKEN>` -- токен  бота, который можно получить у официального бота сервиса Telegram для создания ботов: @BotFather.
- `<CONNECTION_TYPE>` -- может принимать значения `'POLLING'` или `'WEBHOOKS'`, в зависимости от желаемого вами типа
- `<WEBHOOK_HOST>` -- адрес вашего webhook хоста (если  выбран тип подключения `'POLLING'`, то можно не заполнять)
- `<WEBAPP_POST>` -- порт вашего webhook хоста (если  выбран тип подключения `'POLLING'`, то можно не заполнять)
- `<MAX_EPOCH>` -- количество эпох для простого neural style transfer
- `<IMAGE_SIZE>` -- размер выходного изображения

_____

По всем вопросам обращаться в телеграм: @MattT16 и на почту: zaelapporagrange@gmail.com

Асинхронна робота з файлами
Пакет aiofile

Для асинхронної роботи з файлами існує низка пакетів. Почнемо розглядати їх з [aiofile](https://github.com/mosquito/aiofile). Він виконує асинхронні операції за підтримки пакета asyncio.

Замість звичної функції open необхідно використовувати async_open. Вона повертає файлоподібні об'єкти python з асинхронними методами.

Методи, що підтримуються:

async def read(length = -1) — читає фрагмент з файлу (за довжини -1 файл буде прочитаний до кінця);
async def write(data) — записує фрагмент у файл;
def seek(offset) — встановлює позицію покажчика файлу;
def tell() — повертає поточну позицію покажчика файлу;
async def readline(size=-1, newline="\\n") — читає фрагменти до нового рядка або EOF ;
def **aiter**() -> LineReader — ітератор по рядках;
def iter_chunked(chunk_size: int = 32768) -> Reader — ітератор по чанках.

☝ Метод readline не оптимальний для невеликих рядків, оскільки не використовує повторно буфер читання. Якщо необхідно читати файл порядково, уникайте використання async_open, замість цього використовуйте LineReader.

Наприклад, наступний код створить файл hello.txt:

import asyncio
from aiofile import async_open

async def main():
async with async_open("hello.txt", 'w+') as afp:
await afp.write("Hello ")
await afp.write("world\\n")
await afp.write("Hello from - async world!")

if **name** == '**main**':
asyncio.run(main())

hello.txt

Hello world
Hello from - async world!

Прочитати "hello.txt" файл можна різним асинхронним підходом.

Підхід await afp.read()

import asyncio
from aiofile import async_open

async def main():
async with async_open("hello.txt", 'r') as afp:
print(await afp.read())

if **name** == '**main**':
asyncio.run(main())

Підхід async for

import asyncio
from aiofile import async_open

async def main():
async with async_open("hello.txt", 'r') as afp:
async for line in afp:
print(line)

if **name** == '**main**':
asyncio.run(main())

Виведення буде однаковим:

Hello world
Hello from - async world!

LineReader — помічник, який дуже ефективний, коли необхідно прочитати файл лінійно та порядково. Він містить буфер і зчитуватиме фрагменти файлу частинами в буфер, де намагатиметься знайти рядки. Розмір фрагмента за замовчуванням складає 4 КБ.

import asyncio
from aiofile import AIOFile, LineReader

async def main():
async with AIOFile("hello.txt", 'r') as afp:
async for line in LineReader(afp):
print(line)

if **name** == '**main**':
asyncio.run(main())

Виведення:

Hello world

Hello from - async world!

Пакет aiopath

Якщо ви пишете асинхронний код Python і хочете скористатися перевагами pathlib, але не хочете змішувати блокуюче та неблокуюче введення-виведення, можете звернутися до [aiopath](https://github.com/alexdelorenzo/aiopath). API aiopath прямо збігається з API pathlib, але всі необхідні методи асинхронні.

Наприклад, перевіримо, чи існує файл "hello.txt" у поточній директорії:

import asyncio
from aiopath import AsyncPath

async def main():
apath = AsyncPath("hello.txt")
print(await apath.exists())
print(await apath.is_file())
print(await apath.is_dir())

if **name** == '**main**':
asyncio.run(main())

Якщо файл є, виведення буде наступним:

True
True
False

Пакет aioshutil

Бібліотека [aioshutil](https://github.com/kumaraditya303/aioshutil) надає асинхронну версію функції модуля Shutil. Модуль Shutil є синхронним, його використання в асинхронних застосунках заблокує цикл подій і уповільнить роботу застосунку. aioshutil же надає асинхронні дружні версії функцій модуля Shutil.

Для прикладу створимо папку logs та скопіюємо туди файл "hello.txt":

import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile

async def main():
apath = AsyncPath("hello.txt")
if await apath.exists():
new_path = AsyncPath('logs')
await new_path.mkdir(exist_ok=True, parents=True)
await copyfile(apath, new_path / apath)

if **name** == '**main**':
asyncio.run(main())

Асинхронна робота з файлами є потужним інструментом для оптимізації та покращення продуктивності програм. Вона дозволяє ефективно обробляти операції введення-виведення (I/O) з файлами, забезпечуючи швидкість та ефективність виконання.

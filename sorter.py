import asyncio
import argparse
import logging
from aiopath import AsyncPath
from aioshutil import copyfile

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('file_sorter')

async def read_folder(source_folder: AsyncPath):
    """
    Асинхронно получает все файлы из исходной папки и подпапок
    
    Args:
        source_folder: Путь к исходной папке
        
    Returns:
        Список путей к файлам
    """
    files = []
    try:
        async for item in source_folder.glob('**/*'):
            if await item.is_file():
                files.append(item)
    except Exception as e:
        logger.error(f"Ошибка при чтении папки {source_folder}: {e}")
    
    return files

async def copy_file(file_path: AsyncPath, dest_folder: AsyncPath):
    """
    Копирует файл в соответствующую подпапку целевой директории
    
    Args:
        file_path: Путь к исходному файлу
        dest_folder: Путь к целевой папке
    """
    try:
        # Получаем расширение файла (без точки в начале)
        extension = file_path.suffix
        if extension:
            extension = extension[1:].lower()  # Убираем точку и приводим к нижнему регистру
        else:
            extension = "no_extension"
        
        # Создаем подпапку для этого расширения
        extension_folder = dest_folder / extension
        await extension_folder.mkdir(exist_ok=True, parents=True)
        
        # Берем только имя файла, без полного пути
        file_name = file_path.name
        dest_file_path = extension_folder / file_name
        
        # Копируем файл
        await copyfile(file_path, dest_file_path)
        logger.info(f"Скопирован файл {file_path.name} в {extension_folder}")
    except Exception as e:
        logger.error(f"Ошибка при копировании файла {file_path}: {e}")

async def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Асинхронная сортировка файлов по расширениям')
    parser.add_argument('--source', '-s', required=True, help='Исходная директория с файлами')
    parser.add_argument('--output', '-o', required=True, help='Директория для отсортированных файлов')
    
    args = parser.parse_args()
    
    # Инициализируем асинхронные пути
    source_folder = AsyncPath(args.source)
    output_folder = AsyncPath(args.output)
    
    # Проверяем существование папок
    if not await source_folder.exists():
        logger.error(f"Исходная папка {args.source} не существует")
        return
    
    # Создаем выходную папку, если не существует
    await output_folder.mkdir(exist_ok=True, parents=True)
    
    # Получаем все файлы из исходной папки
    files = await read_folder(source_folder)
    logger.info(f"Найдено {len(files)} файлов для сортировки")
    
    # Создаем и запускаем задачи для копирования файлов
    tasks = [copy_file(file_path, output_folder) for file_path in files]
    await asyncio.gather(*tasks)
    
    logger.info("Сортировка завершена")

if __name__ == "__main__":
    asyncio.run(main()) 
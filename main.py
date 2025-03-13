import asyncio
import argparse
import logging
from aiopath import AsyncPath
from aioshutil import copyfile


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('file_sorter')

async def read_folder(source_folder: AsyncPath):
    files = []
    try:
        async for item in source_folder.glob('**/*'):
            if await item.is_file():
                files.append(item)
    except Exception as e:
        logger.error(f"Reading folder error {source_folder}: {e}")
    
    return files


async def copy_file(file_path: AsyncPath, dest_folder: AsyncPath):
    try:
        extension = file_path.suffix
        if extension:
            extension = extension[1:].lower()
        else:
            extension = "no_extension"
        
        extension_folder = dest_folder / extension
        await extension_folder.mkdir(exist_ok=True, parents=True)
        
        # Extract only the filename without full path
        file_name = file_path.name
        dest_file_path = extension_folder / file_name
        
        await copyfile(file_path, dest_file_path)
        logger.info(f"File {file_name} was copied to {extension_folder}")
    except Exception as e:
        logger.error(f"Copying file error {file_path}: {e}")

async def main():
    parser = argparse.ArgumentParser(description='Async file sorting by extensions')
    parser.add_argument('--source', '-s', required=True, help='Source directory with files')
    parser.add_argument('--output', '-o', required=True, help='Directory for sorted files')
    
    args = parser.parse_args()
    
    source_folder = AsyncPath(args.source)
    output_folder = AsyncPath(args.output)
    
    if not await source_folder.exists():
        logger.error(f"Source folder {args.source} does not exist")
        return
    
    await output_folder.mkdir(exist_ok=True, parents=True)
    
    files = await read_folder(source_folder)
    logger.info(f"Found {len(files)} files to sort")
    
    tasks = [copy_file(file_path, output_folder) for file_path in files]
    await asyncio.gather(*tasks)
    
    logger.info("Finished")

if __name__ == "__main__":
    asyncio.run(main()) 
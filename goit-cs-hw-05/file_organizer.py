# Run command to execute the script: python file_organizer.py "." "./organized_files"


import asyncio
import argparse
import logging
import shutil
from pathlib import Path
from typing import List


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('file_organizer.log'),
            logging.StreamHandler()
        ]
    )


async def read_folder(source_path: Path) -> List[Path]:
    """
    Recursively read all files from the source folder and its subfolders.

    Args:
        source_path: Path to the source directory

    Returns:
        List of file paths found in the source directory
    """
    files = []
    try:
        if not source_path.exists():
            logging.error(f"Source path does not exist: {source_path}")
            return files

        if not source_path.is_dir():
            logging.error(f"Source path is not a directory: {source_path}")
            return files

        # Use rglob to recursively find all files
        for file_path in source_path.rglob('*'):
            if file_path.is_file():
                files.append(file_path)
                logging.info(f"Found file: {file_path}")

    except Exception as e:
        logging.error(f"Error reading folder {source_path}: {e}")

    return files


async def copy_file(file_path: Path, output_path: Path) -> None:
    """
    Copy file to the appropriate subdirectory based on its extension.

    Args:
        file_path: Path to the source file
        output_path: Path to the output directory
    """
    try:
        # Get file extension (without the dot)
        extension = file_path.suffix.lower().lstrip('.')

        # If no extension, use 'no_extension' folder
        if not extension:
            extension = 'no_extension'

        # Create target directory path
        target_dir = output_path / extension
        target_dir.mkdir(parents=True, exist_ok=True)

        # Create target file path
        target_file = target_dir / file_path.name

        # Handle duplicate filenames
        counter = 1
        original_target = target_file
        while target_file.exists():
            stem = original_target.stem
            suffix = original_target.suffix
            target_file = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        # Copy file asynchronously (using asyncio.to_thread for I/O operation)
        await asyncio.to_thread(shutil.copy2, file_path, target_file)
        logging.info(f"Copied {file_path} to {target_file}")

    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")


async def organize_files(source_path: Path, output_path: Path) -> None:
    """
    Main function to organize files from source to output directory.

    Args:
        source_path: Path to the source directory
        output_path: Path to the output directory
    """
    try:
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Read all files from source directory
        files = await read_folder(source_path)

        if not files:
            logging.warning("No files found in the source directory")
            return

        logging.info(f"Found {len(files)} files to organize")

        # Create tasks for copying files concurrently
        tasks = [copy_file(file_path, output_path) for file_path in files]

        # Execute all copy operations concurrently
        await asyncio.gather(*tasks, return_exceptions=True)

        logging.info("File organization completed successfully")

    except Exception as e:
        logging.error(f"Error in organize_files: {e}")


def main() -> None:
    """Main entry point of the script."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Organize files by extension asynchronously"
    )
    parser.add_argument(
        "source",
        type=str,
        help="Source directory path"
    )
    parser.add_argument(
        "output",
        type=str,
        help="Output directory path"
    )

    # Parse arguments
    args = parser.parse_args()

    # Set up logging
    setup_logging()

    # Convert string paths to Path objects
    source_path = Path(args.source)
    output_path = Path(args.output)

    logging.info(f"Starting file organization from {source_path} to {output_path}")

    # Run the async function
    try:
        asyncio.run(organize_files(source_path, output_path))
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

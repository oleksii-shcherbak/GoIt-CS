import time
from pathlib import Path
from pprint import pprint
from threaded import threaded_search
from multiprocessed import multiprocess_search

def load_files(directory: str) -> list[str]:
    """Recursively loads all .txt files from the specified directory.

    Args:
        directory (str): Path to the folder containing text files.

    Returns:
        list[str]: List of full file paths to .txt files found in the directory.
    """
    return [str(p) for p in Path(directory).rglob("*.txt")]

if __name__ == "__main__":
    folder = "text_samples"
    keywords = ["truth", "freedom", "grief", "dream", "name", "cossack", "mother", "sky"]

    filepaths = load_files(folder)

    print(f"Total files: {len(filepaths)}")
    print(f"Keywords: {keywords}\n")

    # Threaded version
    start = time.perf_counter()
    result_threads = threaded_search(filepaths, keywords)
    end = time.perf_counter()
    print("Threaded version result:")
    pprint(result_threads)
    print(f"Time (threaded): {end - start:.5f} seconds\n")

    # Multiprocessed version
    start = time.perf_counter()
    result_mp = multiprocess_search(filepaths, keywords)
    end = time.perf_counter()
    print("Multiprocessing version result:")
    pprint(result_mp)
    print(f"Time (multiprocessing): {end - start:.5f} seconds")

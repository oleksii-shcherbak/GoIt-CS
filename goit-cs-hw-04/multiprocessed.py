import multiprocessing
from typing import List, Dict
from multiprocessing import Queue

def search_keywords_in_file(filepath: str, keywords: List[str]) -> Dict[str, List[str]]:
    """Searches for given keywords in a single text file.

    Args:
        filepath (str): Path to the file to search in.
        keywords (List[str]): List of lowercase keywords to search for.

    Returns:
        Dict[str, List[str]]: A dictionary where each found keyword maps to a list
        containing the file path (once per keyword if found).
    """
    result = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    result.setdefault(keyword, []).append(filepath)
    except (OSError, UnicodeDecodeError):
        pass
    return result

def mp_worker(files: List[str], keywords: List[str], queue: Queue) -> None:
    """Worker function to be run inside a separate process.

    It searches for keywords across the assigned files and sends the result
    dictionary back to the parent process via a queue.

    Args:
        files (List[str]): A list of file paths to the process.
        keywords (List[str]): List of keywords to search for in each file.
        queue (Queue): A multiprocessing queue used to send results back to the parent.
    """
    result = {}
    for path in files:
        partial = search_keywords_in_file(path, keywords)
        for word, matches in partial.items():
            result.setdefault(word, []).extend(matches)
    queue.put(result)

def multiprocess_search(filepaths: List[str], keywords: List[str]) -> Dict[str, List[str]]:
    """Performs a parallel keyword search across multiple files using multiprocessing.

    Files are split among multiple processes based on the number of available CPU cores.
    Each process performs the search and returns its partial result via a multiprocessing queue.

    Args:
        filepaths (List[str]): List of paths to text files to be scanned.
        keywords (List[str]): List of keywords to search for in each file.

    Returns:
        Dict[str, List[str]]: A dictionary where each key is a keyword, and the value is a
        list of file paths in which that keyword was found.
    """
    result = {}
    queue = multiprocessing.Queue()

    processes = []
    cpu_count = multiprocessing.cpu_count()
    chunk_size = len(filepaths) // cpu_count or 1

    for i in range(0, len(filepaths), chunk_size):
        p = multiprocessing.Process(target=mp_worker, args=(filepaths[i:i+chunk_size], keywords, queue))
        p.start()
        processes.append(p)

    for _ in processes:
        partial = queue.get()
        for word, matches in partial.items():
            result.setdefault(word, []).extend(matches)

    for p in processes:
        p.join()

    return result

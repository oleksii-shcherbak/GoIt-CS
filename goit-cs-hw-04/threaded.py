import threading
from typing import List, Dict

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

def threaded_search(filepaths: List[str], keywords: List[str]) -> Dict[str, List[str]]:
    """Performs a parallel keyword search across multiple files using threads.

    Each thread processes a subset of files and aggregates results into a shared dictionary
    with thread-safe access.

    Args:
        filepaths (List[str]): List of paths to text files to be scanned.
        keywords (List[str]): List of keywords to search for in each file.

    Returns:
        Dict[str, List[str]]: A dictionary where each key is a keyword, and the value is a
        list of file paths in which that keyword was found.
    """
    result = {}
    lock = threading.Lock()

    def worker(files: List[str]):
        """Worker function for a single thread to process a chunk of files.

        Args:
            files (List[str]): A list of file paths assigned to this thread.
        """
        local_result = {}
        for path in files:
            partial = search_keywords_in_file(path, keywords)
            for word, matches in partial.items():
                local_result.setdefault(word, []).extend(matches)
        with lock:
            for word, matches in local_result.items():
                result.setdefault(word, []).extend(matches)

    threads = []
    chunk_size = len(filepaths) // 4 or 1
    for i in range(0, len(filepaths), chunk_size):
        t = threading.Thread(target=worker, args=(filepaths[i:i+chunk_size],))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return result

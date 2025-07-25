import string
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple
from urllib.error import URLError

import matplotlib.pyplot as plt


def map_function(text: str) -> List[Tuple[str, int]]:
    """
    Map function that processes text and returns word-count pairs.

    Args:
        text: Input text to process

    Returns:
        List of (word, 1) tuples
    """
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Split into words and filter out empty strings and short words
    words = [word.strip() for word in text.split() if len(word.strip()) > 2]

    return [(word, 1) for word in words if word]


def shuffle_function(mapped_values: List[Tuple[str, int]]) -> List[Tuple[str, List[int]]]:
    """
    Shuffle function that groups mapped values by key.

    Args:
        mapped_values: List of (word, count) tuples

    Returns:
        List of (word, [counts]) tuples
    """
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return list(shuffled.items())


def reduce_function(shuffled_values: List[Tuple[str, List[int]]]) -> Dict[str, int]:
    """
    Reduce function that sums up counts for each word.

    Args:
        shuffled_values: List of (word, [counts]) tuples

    Returns:
        Dictionary with word frequencies
    """
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced


def map_reduce(text: str) -> Dict[str, int]:
    """
    Execute MapReduce operation on text.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary with word frequencies
    """
    # Step 1: Mapping
    mapped_values = map_function(text)

    # Step 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Step 3: Reduction
    reduced_values = reduce_function(shuffled_values)

    return reduced_values


def map_reduce_parallel(text: str, num_workers: int = 4) -> Dict[str, int]:
    """
    Execute MapReduce operation on text with multithreading.

    Args:
        text: Input text to analyze
        num_workers: Number of worker threads

    Returns:
        Dictionary with word frequencies
    """
    # Split text into chunks for parallel processing
    text_length = len(text)
    chunk_size = max(text_length // num_workers, 1)
    chunks = []

    for i in range(num_workers):
        start = i * chunk_size
        if i == num_workers - 1:
            # Last chunk gets remaining text
            end = text_length
        else:
            end = (i + 1) * chunk_size
        chunks.append(text[start:end])

    # Map phase - process chunks in parallel
    all_mapped_values = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        mapped_results = list(executor.map(map_function, chunks))

    # Combine all mapped values
    for mapped_chunk in mapped_results:
        all_mapped_values.extend(mapped_chunk)

    # Shuffle phase
    shuffled_values = shuffle_function(all_mapped_values)

    # Reduce phase
    reduced_values = reduce_function(shuffled_values)

    return reduced_values


def download_text(url: str) -> str:
    """
    Download text content from URL.

    Args:
        url: URL to download from

    Returns:
        Downloaded text content

    Raises:
        URLError: If download fails
    """
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
        return content
    except URLError as e:
        raise URLError(f"Failed to download from {url}: {e}")


def visualize_top_words(word_freq: Dict[str, int], top_n: int = 10) -> None:
    """
    Visualize top N words by frequency using a horizontal bar chart.

    Args:
        word_freq: Dictionary with word frequencies
        top_n: Number of top words to display
    """
    # Sort words by frequency and get top N
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:top_n]

    if not top_words:
        print("No words to visualize")
        return

    # Prepare data for plotting
    words = [item[0] for item in top_words]
    frequencies = [item[1] for item in top_words]

    # Create horizontal bar chart
    plt.figure(figsize=(12, 8))
    bars = plt.barh(words, frequencies, color='skyblue', edgecolor='navy', alpha=0.7)

    # Customize the chart
    plt.xlabel('Frequency', fontsize=12)
    plt.ylabel('Words', fontsize=12)
    plt.title(f'Top {top_n} Most Frequent Words', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()  # Invert y-axis to show highest frequency at top

    # Add value labels on bars
    for bar, freq in zip(bars, frequencies):
        plt.text(bar.get_width() + max(frequencies) * 0.01,
                 bar.get_y() + bar.get_height() / 2,
                 str(freq),
                 ha='left', va='center', fontsize=10)

    # Add grid for better readability
    plt.grid(axis='x', alpha=0.3)

    # Adjust layout and display
    plt.tight_layout()
    plt.show()

    # Print top words
    print(f"\nTop {top_n} most frequent words:")
    for i, (word, freq) in enumerate(top_words, 1):
        print(f"{i:2d}. {word:15s} - {freq:4d} occurrences")


if __name__ == '__main__':
    # URL to analyze (you can change this to any text URL)
    url = "https://www.gutenberg.org/cache/epub/68486/pg68486.txt"  # Kobzar by Taras Shevchenko

    try:
        print("Downloading text from URL...")
        text = download_text(url)
        print(f"Downloaded {len(text)} characters")

        print("Analyzing word frequencies using MapReduce...")

        # Use parallel MapReduce for better performance
        word_frequencies = map_reduce_parallel(text, num_workers=4)

        print(f"Found {len(word_frequencies)} unique words")

        # Visualize results
        visualize_top_words(word_frequencies, top_n=10)

    except URLError as e:
        print(f"Error downloading text: {e}")
        print("Using sample text instead...")

        # Fallback to sample text if URL fails
        sample_text = "hello world hello Python hello Student " * 100
        word_frequencies = map_reduce(sample_text)
        print("Sample text analysis result:", word_frequencies)
        visualize_top_words(word_frequencies, top_n=10)

    except Exception as e:
        print(f"An error occurred: {e}")

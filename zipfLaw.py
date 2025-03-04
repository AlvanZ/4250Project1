import os
from collections import Counter
import matplotlib.pyplot as plt
import csv

def load_tokenized_files(directory):
    """Load tokenized files from the directory and return a list of words."""
    words = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf8') as f:
                words.extend(f.read().split())
    return words

def calculate_word_frequencies(words):
    """Calculate the frequency of each word."""
    word_freq = Counter(words)  # Count word frequencies
    return word_freq

def save_top_words(sorted_words, domain, output_file):
    """Save the top 50 words, their ranks, and frequencies to a CSV file."""
    top_50_words = sorted_words[:50]
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Rank", "Word", "Frequency"])  # Write header in the table csv file
        for rank, (word, freq) in enumerate(top_50_words, start=1):
            writer.writerow([f"{rank:>4}", f"{word:<15}", f"{freq:>8}"]) #readable in csv file

def plot_zipfs_law(ranks, frequencies, domain):
    """Plot Zipf's Law: Frequency vs Rank on a log-log scale."""
    plt.figure(figsize=(8, 6))
    plt.loglog(ranks, frequencies, marker='o', linestyle='none', label=f'Zipf\'s Law ({domain})')
    plt.xlabel('Rank (log scale)')
    plt.ylabel('Frequency (log scale)')
    plt.title(f"Zipf's Law - {domain}")
    plt.legend()
    plt.grid(True) # readability
    plt.savefig(f"zipfLaw_{domain.replace('/', '_')}.png")  # Save plot as PNG
    plt.show()

def zipfs_law_analysis(directory, domain, output_file):
    """Perform Zipf's Law analysis for a given domain."""
    # Step 1: Load tokenized words
    words = load_tokenized_files(directory)
    
    # Step 2: Calculate word frequencies
    word_freq = calculate_word_frequencies(words)
    
    # Step 3: Sort words by frequency in descending order
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Step 4: Save top 50 words to CSV
    save_top_words(sorted_words, domain, output_file)
    
    # Step 5: Plot Zipf's Law
    ranks = range(1, len(sorted_words) + 1)
    frequencies = [freq for _, freq in sorted_words]
    plot_zipfs_law(ranks, frequencies, domain)

# Directories to process (replace with your tokenized directories)
directories = {
    "cpp.edu/EN": "tokenized/cpp.edu/EN",       # Words1.csv
    "taobao.com/ZH": "tokenized/taobao.com/ZH",  # Words2.csv
    "yahoo.co.jp/JA": "tokenized/yahoo.co.jp/JA"     # Words3.csv
}

# Perform Zipf's Law analysis for each domain
for domain, directory in directories.items():
    if os.path.exists(directory):
        output_file = f"Words{list(directories.keys()).index(domain) + 1}.csv"
        zipfs_law_analysis(directory, domain, output_file)
import os
import matplotlib.pyplot as plt

def vocabularyGrowth(directory):
    vocab = set()  # Tracks unique words
    total_words = 0  # Tracks total words processed
    growth = []  # Stores (total_words, vocabulary_size) pairs
    
    print(f"Processing directory: {directory}")
    
    # Loop through each file in the directory
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        print(f"Processing file: {file_path}")
        
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf8', errors='ignore') as f:
                words = f.read().split()  # Split text into words
                for word in words:
                    vocab.add(word)  # Add word to vocabulary set
                    total_words += 1  # Increment total word count
                    growth.append((total_words, len(vocab)))  # Record growth
    
    print(f"Total words: {total_words}, Vocabulary size: {len(vocab)}")
    return growth

def plot_heaps_law(domain, growth):
    if not growth:
        print(f"No data to plot for {domain}")
        return
    
    # Unzip the growth data into x (total_words) and y (vocabulary_size)
    x, y = zip(*growth)
    
    # Plot the data
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'Vocabulary Growth ({domain})')
    plt.xlabel("Total Words")
    plt.ylabel("Vocabulary Size")
    plt.title(f"Heap's Law - {domain}")
    plt.legend()
    plt.grid()
    plt.savefig(f"heapLaw_{domain.replace('/', '_')}.png")  # Save plot as PNG
    plt.show()

# Directories to process
directories = ["stemmed/taobao.com/ZH", "stemmed/cpp.edu/EN", "stemmed/yahoo.co.jp/JA"]

# Generate Heap's Law plots for each domain
for directory in directories:
    if os.path.exists(directory):
        growth = vocabularyGrowth(directory)
        plot_heaps_law(directory, growth)

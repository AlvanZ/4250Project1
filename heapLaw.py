import os
import matplotlib.pyplot as plt

def count_vocabulary_growth(directory):
    vocab = set()
    total_words = 0
    growth = []
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        
        # Ensure it's a file before opening
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf8', errors='ignore') as f:
                words = f.read().split()
                for word in words:
                    vocab.add(word)
                    total_words += 1
                    growth.append((total_words, len(vocab)))
    
    return growth

def plot_heaps_law(domain, growth):
    if not growth:
        print(f"No data to plot for {domain}")
        return
    
    x, y = zip(*growth)
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'Vocabulary Growth ({domain})')   #?
    plt.xlabel("Total Words")
    plt.ylabel("Vocabulary)")
    plt.title(f"Heap's Law - {domain}")
    plt.legend()
    plt.grid()
    plt.show()


directories = ["cpp.edu","taobao.com", "yahoo.co.jp"]  # Update directories
for directory in directories:
    if os.path.exists(directory):
        growth = count_vocabulary_growth(directory)
        plot_heaps_law(directory, growth)

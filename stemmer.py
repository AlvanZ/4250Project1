import os
from nltk.stem import PorterStemmer
from jpstemmer import JPStemmer
from langdetect import detect

def detect_language(text):
    """
    Detects the language of a given text.
    
    Args:
        text: A string containing words.
    
    Returns:
        'ja' if Japanese, 'en' if English, otherwise None.
    """
    try:
        lang = detect(text)
        return lang
    except:
        return None  # Return None if detection fails

def stem_file(input_path, output_path):
    """
    Stem all words in the input file and write results to the output file.
    
    Args:
        input_path: Path to the input file with tokenized words (one per line)
        output_path: Path to save the stemmed words (one per line)
    """
    
    # Read words from input file
    with open(input_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file if line.strip()]
    
    # Detect language of the first few words (assumes all words in file are the same language)
    sample_text = " ".join(words[:10])  # Use a sample of the first 10 words
    language = detect_language(sample_text)

    if language == 'ja':
        stemmer = JPStemmer()
        stemmed_words = [stemmer.stemmer(word) for word in words]
    else:
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in words]

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write stemmed words to output file
    with open(output_path, 'w', encoding='utf-8') as file:
        for word in stemmed_words:
            file.write(word + '\n')

def process_all_files():
    """Process all files in the tokenized folder and save results to the stemmed folder."""

    dirs = ["cpp.edu/EN", "taobao.com/JA", "taobao.com/ZH", "yahoo.co.jp/JA"]

    for dir in dirs:
        os.makedirs(f"stemmed/{dir}", exist_ok=True)
        for filename in os.listdir(f"tokenized/{dir}"):
            if filename.endswith('.txt'):
                input_path = os.path.join(f"tokenized/{dir}", filename)
                output_path = os.path.join(f"stemmed/{dir}", filename)
                
                print(f"Processing {filename}...")
                stem_file(input_path, output_path)
                print(f"Stemmed words saved to {output_path}")

  

if __name__ == "__main__":
    process_all_files()
    print("All files have been processed successfully!")
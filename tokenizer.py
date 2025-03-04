import os
import re
from tqdm import tqdm
from bs4 import BeautifulSoup

def main():
    dirs = ["cpp.edu/EN", "taobao.com/JA", "taobao.com/ZH", "yahoo.co.jp/JA"]

    for dir in dirs:
        os.makedirs(f"tokenized/{dir}", exist_ok=True)
        tokenize(dir)

def tokenize(path):
    # loop through each file within the specificed folder, using tqdm to display progress
    for file in tqdm(os.listdir(path)):
        # open the file and extract the raw html from it
        opened_file = open(f"{path}/{file}", "r", encoding="utf8")
        raw_html = opened_file.read()

        # use Beautiful Soup to parse the html
        soup = BeautifulSoup(raw_html, features="html.parser")

        # remove all script and style elements from the html
        for script in soup(["script", "style"]):
            script.extract()

        # get the text from the html, separating by new lines and removing trailing spaces
        text = soup.get_text(separator="\n", strip=True)

        # use regex to remove all non-alphanumeric characters (except for new lines) from the text and replace them with spaces
        #text = re.sub(r'[^\w\n]', ' ', text)

        # split the text by spaces and new lines into a list of words
        words = text.split()

        # join all the words together, putting a new line between each word
        text = "\n".join(words)

        # create a new file for the tokenized document
        tokenized_file = open(f"tokenized/{path}/{file}", "w", encoding="utf8")

        # write the new tokenized document onto the new file
        tokenized_file.write(text)

        # close the files
        opened_file.close()
        tokenized_file.close()

if __name__ == "__main__":
    main()
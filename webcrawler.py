import os
# 1. Make method to get the seed url
# 2. GO to page, error handle if it doesn't exist. Then you save that page
# 3. Check if page is in set, if not then add it and then go through all anchor tags that contain the seed url
# 4. Recurse to 2
# Needs set to prevent duplicates, and then language detection.



def count_html_files(directory):
    return sum(1 for file in os.listdir(directory) if file.endswith(".html"))


def run(pages: int, directoryLocation: str):
    if(count_html_files(directoryLocation)==pages):
        return "Job Done"

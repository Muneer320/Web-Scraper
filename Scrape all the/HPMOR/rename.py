import re
import os

# Define the pattern to match the filename and capture the relevant parts
pattern = re.compile(r'^.*The Methods Of Rationality： Chapter ([\d-]+[a-z]?) \[.*\]\.mp3$')

# Function to rename the files
def rename_files(directory):
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            chapter_number = match.group(1).replace("-", " & ")
            new_filename = f"HPMoR Chapter {chapter_number}.mp3"
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

# Example usage
directory_path = os.getcwd()  # Replace with the path to your files
rename_files(directory_path)

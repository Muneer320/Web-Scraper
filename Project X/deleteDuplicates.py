import os
import hashlib
from collections import defaultdict

# Function to calculate the hash of a file
def calculate_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to delete duplicate images in a directory
def delete_duplicate_images(directory):
    image_hashes = defaultdict(list)
    num_del = 0
    files = sorted(os.listdir(directory)[:-1], key=lambda f: int(os.path.splitext(f)[0]))

    # Traverse the directory and calculate hashes of all image files

    for file in files:
        # Check if the file is an image (you can extend this check to include other image formats)
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(directory, file)
            file_hash = calculate_hash(file_path)
            image_hashes[file_hash].append(file_path)

    # Delete duplicate images, keeping only one copy
    for hash_value, file_paths in image_hashes.items():
        if len(file_paths) > 1:
            print(f"Duplicate images with hash {hash_value}:")
            for file_path in file_paths[1:]:
                print(f"\tDeleting: {file_path}")
                num_del += 1
                os.remove(file_path)
    print(f"{num_del} images deleted.")

# Example usage:
if __name__ == "__main__":
    # directory_path = input("Enter the directory path where you want to delete duplicate images: ")
    directory =  input("Enter the name of the directory to to remove duplicates from (leave blank for default): ")
    DIR = "downloaded_images" if directory == "" else directory
    delete_duplicate_images(DIR) #downloaded_images
    print("Deleted dublicate images!")
input()
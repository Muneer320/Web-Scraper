import os
import string

loc = os.path.join("Project X Downloads", input("Enter the path to the directory: "))
if not os.path.exists(loc):
    print("Directory does not exist.")
    exit


names = [x + y + z for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase]
image_name = input("Enter the starting image name: ")
names = names[names.index(image_name):]

for root, _, files in os.walk(loc):
    for file in files:
        if not file.endswith(".txt"):
            ext = os.path.splitext(file)[1]
            os.rename(os.path.join(root, file), os.path.join(root, f"{names.pop(0)}{ext}"))
            print(f"Renamed: {file}")
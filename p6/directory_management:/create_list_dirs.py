#1
import os
files = os.listdir()
print(files)

#2
import os
files = os.listdir("foldername")
print(files)

#3
import os

dir_name = "my_folder"

if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    print("Directory created")
else:
    print("Directory already exists")

os.makedirs("parent/child/grandchild", exist_ok=True)

print("\nContents of current directory:")
items = os.listdir(".")

for item in items:
    print(item)
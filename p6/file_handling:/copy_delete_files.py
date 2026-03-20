#1
with open("source.txt", "r") as source:
    data = source.read()

with open("copy.txt", "w") as cp:
    cp.write(data)

#2
import shutil

shutil.copy("source.txt", "copy.txt")
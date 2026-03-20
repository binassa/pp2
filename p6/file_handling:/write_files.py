#1
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

with open("demofile.txt") as f:
  print(f.read())

#2
with open("example.txt", "a") as file:
    file.write("\nThis line is added later.")

#3
name = input("Enter your name: ")

with open("names.txt", "a") as file:
    file.write(name + "\n")
#1
f = open("demofile.txt")
print(f.read())

#2
with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline())

#3
with open("demofile.txt") as f:
  for x in f:
    print(x)

#4
f = open("myfile.txt", "x")

#5
with open("example.txt", "r") as file:
    lines = file.readlines()

print(lines)
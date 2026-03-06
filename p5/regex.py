#1
import re
text = input()
matches = re.findall(r"ab*", text)
print(matches)

#2
import re
text = input()
matches = re.findall(r"ab{2,3}", text)
print(matches)

#3
import re
text = input()
matches = re.findall(r"[a-z]+_[a-z]+", text)
print(matches)

#4
import re
text = input()
matches = re.findall(r"[A-Z][a-z]+", text)
print(matches)

#5
import re
text = input()
matches = re.findall(r"a.*?b", text)
print(matches)

#6
import re
text = input()
result = re.sub(r"[ ,.]", ":", text)
print(result)

#7
import re
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)
print(snake_to_camel(text))

#8
import re
text = input()
result = re.split(r"(?=[A-Z])", text)
print(result)

#9
import re
text = input()
result = re.sub(r"([A-Z])", r" \1", text).strip()
print(result)

#10
import re
text = input()
result = re.sub(r"([A-Z])", r"_\1", text).lower()
print(result)

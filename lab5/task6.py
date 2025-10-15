import re
text=input()
new_text = re.sub(r"[\s,\.]", ":", text)
print(new_text)
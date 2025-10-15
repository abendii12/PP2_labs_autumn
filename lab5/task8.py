import re
a=input()
result = re.findall(r'[a-z]+|[A-Z][a-z]*', a)
print(result)
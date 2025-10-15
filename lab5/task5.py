import re
text=input()
if re.search("a+[a-z]*b+",text):
    print ("True")
else:
    print("False")
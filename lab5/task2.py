import re
text=input()
if re.search("a+b{2,3}$",text):
    print ("True")
else:
    print("False")
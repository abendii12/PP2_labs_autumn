list = ["PP2", "Algorithms", "Economics", "Information systems", "Database design", "PE"]
file = open(r'C:\Users\abend\OneDrive\Documents\PP2_labs_2025\labs\lab6\dir\text.txt','w')
for subject in list:
    file.write(subject + "\n")
    
file.close()
print("ok")
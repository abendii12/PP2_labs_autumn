first_file = r"C:\Users\abend\OneDrive\Documents\PP2_labs_2025\labs\lab6\dir\text.txt"
second_file = r"C:\Users\abend\OneDrive\Documents\PP2_labs_2025\labs\lab6\dir\copy.txt"
file = open(first_file, "r")
reading = file.read()
file.close()
file_2 = open(second_file, "w")
copying = file_2.write(reading)
file_2.close()
print("that is all")


for i in range(26):
    letter = chr(65 + i)
    filename = letter + ".txt"
    file = open(filename, "w")
    file.write(f"This is file {filename}")
    file.close()
    
print("That is all")
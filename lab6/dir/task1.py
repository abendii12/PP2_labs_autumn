import os 
path = r"C:\Users\abend\OneDrive\Documents\PP2_labs_2025\labs\lab6\dir"
print("All:", [name for name in os.listdir(path)])
print("Folders:", [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])
print("Files:", [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name)) ])
import os
path = r"C:\Users\abend\OneDrive\Documents\PP2_labs_2025\labs\lab6\dir\task1.py"
def checking(path):
    print("Exists:", os.path.exists(path))
    print("Readable:", os.access(path, os.R_OK))
    print("Writable:", os.access(path, os.W_OK))
    print("Executable:", os.access(path, os.X_OK))
    
checking(path)
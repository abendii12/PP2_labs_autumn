import os
file_path = r"C:\Users\abend\OneDrive\Documents\PP2_labs_2025\labs\lab6\dir\fordelete.txt" 

if os.path.exists(file_path):
    if os.access(file_path, os.R_OK) and os.access(file_path, os.W_OK):
        os.remove(file_path)  
        print(f"File '{file_path}' has been successfully deleted.")
    else:
        print(f"Access denied: Unable to delete '{file_path}'.")
else:
    print(f"File '{file_path}' does not exist.")
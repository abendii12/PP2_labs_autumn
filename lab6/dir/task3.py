import os
path = r"C:\Users\abend\OneDrive\Documents\PP2_labs_2025\labs\lab6\dir\task2.py"
if os.path.exists(path):
    print("The path exists")
    direc = os.path.dirname(path)
    name = os.path.basename(path)
    print("Filename:", name)
    print("Directory portion:", direc)
    
else:
    print("The path does not exist")
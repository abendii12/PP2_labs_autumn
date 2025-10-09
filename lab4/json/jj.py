import json
file_path = "C:/Users/abend/OneDrive/Documents/PP2_labs_2025/labs/sample-data.json"
with open(file_path, "r") as file:
    data = json.load(file)
    
print("""Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------""")

for i in data["imdata"]:
    dn_key=i["l1PhysIf"]["attributes"]["dn"]
    descr_key=i["l1PhysIf"]["attributes"]["descr"]
    speed_key=i["l1PhysIf"]["attributes"]["speed"]
    mtu_key=i["l1PhysIf"]["attributes"]["mtu"]
    
    
    print(f"{dn_key:<50} {descr_key:<20} {speed_key:<9} {mtu_key:<8}")
    
    
    

    
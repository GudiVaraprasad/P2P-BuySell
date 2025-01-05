# Mac Users: run_nodes.py
import subprocess
import os
import random
import json

data={"boar":{"quantity":0, "price":0},"fish":{"quantity":0, "price":0},"salt":{"quantity":0, "price":0}}
types = ["Boars", "Salt", "Fish"]

with open("stock.json", "w") as file:
    json.dump(data, file, indent=4) 


cwd = os.getcwd()


no_of_nodes= int(input("No of nodes: "))
numbers = [i for i in range(1, no_of_nodes+1)] 
with open("config_buyers_sellers.json", "r") as file:
        buyers_sellers = json.load(file)
 

sellers = buyers_sellers[str(no_of_nodes)]["sellers"]
if os.name == "nt":
    commands = [
    ["python", f"{cwd}\\peer.py", str(i), "seller" if i in sellers else "buyer", str(no_of_nodes)]
    for i in range(1, no_of_nodes + 1)
    ]
    commands.append(["python", f"{cwd}\\warehouse.py", str(51)])
    print(commands)

    # Start processes in new cmd windows
    for cmd in commands:
        try:
            
            # Full command for Windows cmd.exe
            full_command = (
                f"start cmd /k \"{' '.join(cmd)}\""
            )
            
            print(f"Executing: {full_command}")  # Debugging output
            subprocess.Popen(full_command, shell=True)
        except Exception as e:
            print(f"Failed to start process: {' '.join(cmd)} - {e}") 

if os.name == "posix":

    commands=[["python", f"{cwd}/peer_cache.py", str(i), "seller" if i in sellers else "buyer", str(no_of_nodes)] for i in range(1,no_of_nodes+1)]
    commands.append(["python", f"{cwd}/warehouse.py", str(51)])
    # print(commands)

    for cmd in commands:
        try:       
        
            # Construct the full command to execute in a new terminal
            full_command = (
                f"osascript -e 'tell app \"Terminal\" to do script "
                f"\" source {cwd}/venv/bin/activate && {' '.join(cmd)}\"'"
            )
            # Execute the command in a new terminal
            subprocess.Popen(full_command, shell=True)
            
        except Exception as e:
            # Log failure to start the process
            print(f"Failed to start process: {' '.join(cmd)} - {e}")

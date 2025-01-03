import os
import shutil
import subprocess
import re
from collections import defaultdict

modDefs = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.txt'):
        modDefs.append(file)

if len(modDefs) == 0:
    print("No .txt files found! Place the mod definitions in the same folder as this script.")
else:
    print("----------------------------Select which mod to assemble".ljust(100, "-"))
    for i in range(modDefs.__len__()):
        print(str(i + 1) + ": " + modDefs[i])
    selection = input("Select: ")
    validSelection = False
    try:
        selection = int(selection) - 1
        if selection < 0 or selection > modDefs.__len__() - 1:
            print("Invalid selection.")
        else:
            validSelection = True
    except:
        print("Invalid selection.")

modFile = modDefs[selection]
modName = modFile.replace(".txt","")

with open(modFile) as f:
    with open(".gitignore", "w") as gi:
        gi.write("*\n")
        gi.write("!Illustrations/*\n")
        gi.write("!*.png\n")
        gi.write("!.gitignore\n")
        gi.write("!*.py\n")
        gi.write("!*.txt\n")
        gi.write("!*.md\n")
        for line in f.readlines():
            if "#" not in line and len(line.strip()) > 0: 
                asset = line.replace("frostpunk2://content/Game/", "").strip()
                gi.write("!" + asset + ".*\n")
            else:
                #Change context
                if "#" in line and "SEPARATE" in line:
                    context = line.replace("SEPARATE", "").replace("#", "").replace(" ", "").strip()
                else:
                    context = "Core"
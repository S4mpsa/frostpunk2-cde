contentFolder = r'D:\Games\FrostKit\FrostKit\UE4\p10\Saved\Cooked\Windows\Frostpunk2\Content'
cookerScript = r'D:\Games\FrostKit\FrostKit\Frostpunk2IncrementalCooker.bat'

import os
import shutil
import subprocess
import re
from collections import defaultdict

def cookUntilRequired(files):
    print("Starting cooking")
    cooker = subprocess.Popen(shell=True, args = cookerScript, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    filesRemaining = files.copy()
    totalCount = len(filesRemaining)
    while True:
        line = cooker.stdout.readline()
        if b"Packages Remain" in line:
            values = re.findall(r'\d+', str(line))
            print("Cooking process: {}%".format(int((int(values[0])/int(values[2])) * 100)))
            #Cross off all files that have already been cooked
            for i in range(0, len(filesRemaining)):
                if os.path.exists(os.path.join(contentFolder, filesRemaining[i] + ".uasset")):
                    print("Found " + filesRemaining[i].split("/")[-1])
                    filesRemaining[i] = None
            filesRemaining = [x for x in filesRemaining if x is not None]
            #If no more files remain, stop cooking
            print("Files found: " + str(totalCount - len(filesRemaining)) + "/" + str(totalCount))
            if len(filesRemaining) == 0:
                print("All files have been cooked, terminating!")
                cooker.kill() 
                break
        if not line:
            break

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


def findContext(asset, assemblies: dict):
    for context, assets in assemblies.items():
        if asset in assets:
            return context
    return None


#Create a new folder in the repak folder
modFile = modDefs[selection]
modName = modFile.replace(".txt","")
modFolder = os.path.join(os.getcwd(), modName)
if os.path.exists(modFolder):
    shutil.rmtree(modFolder)

os.makedirs(modFolder)

#Read the selection file one line at a time
assets = []
assemblies = defaultdict(list)
context = "Core"

with open(modFile) as f:
    for line in f.readlines():
        if "#" not in line and len(line.strip()) > 0: 
            asset = line.replace("frostpunk2://content/Game/", "").strip()
            assets.append(asset)
            assemblies[context].append(asset)
        else:
            #Change context
            if "#" in line and "SEPARATE" in line:
                context = line.replace("SEPARATE", "").replace("#", "").replace(" ", "").strip()
            else:
                context = "Core"

cookUntilRequired(assets)

for assetPath in assets:
    assetFolder = "/".join(assetPath.split("/")[0:-1])
    asset = assetPath.split("/")[-1]
    context = findContext(assetPath, assemblies)
    try:

        #Copy the file from cooked files into the new folder, creating the correct path as required
        assetFolderPath = os.path.join(modFolder, context+"/Frostpunk2/Content", assetFolder)
        if not os.path.exists(assetFolderPath):
            os.makedirs(assetFolderPath)
        if "/Levels/" in assetPath:
            shutil.copy(os.path.join(contentFolder, assetPath + ".umap"), os.path.join(assetFolderPath, asset + ".umap"))
            shutil.copy(os.path.join(contentFolder, assetPath + ".uexp"), os.path.join(assetFolderPath, asset + ".uexp"))
        else:
            shutil.copy(os.path.join(contentFolder, assetPath + ".uasset"), os.path.join(assetFolderPath, asset + ".uasset"))
            shutil.copy(os.path.join(contentFolder, assetPath + ".uexp"), os.path.join(assetFolderPath, asset + ".uexp"))
        #print("Packing " + asset)
    except:
        print("Asset not found: " + asset)

#Run repak for each module
os.chdir(modFolder)
for submodule in assemblies:
    subprocess.run(["repak", "pack", submodule])
    #Rename and move the created .pak
    shutil.move(os.path.join(os.getcwd(), submodule + ".pak"), os.path.join(os.getcwd(), "CDE_" + submodule + "_P.pak"))
#Cleanup
for submodule in assemblies:
    if os.path.exists(submodule):
        shutil.rmtree(submodule)
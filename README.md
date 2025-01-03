# City Development Effort

Frostpunk 2 Balance Overhaul

https://mod.io/g/frostpunk2/m/cde

https://www.nexusmods.com/frostpunk2/mods/29

This repository contains the uncooked data assets of City Development Effort. Feel free to build your mod on top of these assets for compatibility, fork and edit them for your custom changes or open a new pull request detailing the changes if you want to contribute to development.

This repository should be cloned within your Frostkit installation, in `FrostKit/UE4/p10/Content`. It will overwrite any existing files you have that CDE also modifies, so make sure to have a backup if you don't want to lose your own files.

To cook CDE, use `assembleMod.py` with the provided `CityDevelopmentEffort.txt` which contains all the assets that should be included. You need `repak` (https://github.com/trumank/repak) to be accessible through the command line and Python 3.x, along with an up-to-date installation of FrostKit. Change the filepaths to point to your installation when cooking.

You can regenerate the `.gitignore` by running `createGitIgnore.py`, which is used to select the assets that should be contained within this repository.
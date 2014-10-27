#Uses:
This lets you edit a tile map file.
It will **not** create and/or modify the tile definition file.
This still needs to be done manually.

#How to run:
python main.py *[definition file path]* *[map file path]*
  
  **If *[map file path]* does not exist then it will be created**

#Keyboard controls:
* ***i*** - toggles info mode
  * makes all mouse clicks equivalent to the default right click behavior
* ***backspace*** - toggles delete mode
  * makes all mouse clicks other than right clicks delete the highlighted tile
* ***Enter/Return*** - saves the map
  * **overwrites anything that used to be in the map file with what is displayed in the editor**
* ***u*** - attempts to undo the last performed action (set/delete)
* ***Escape*** - reloads the tile definition and map files
  * in addition to reloading the tile definition file, this **reverts any unsaved changes**

#Mouse controls:
* ***Right click*** - shows the information for the tile under the cursor (acts as any other click with info mode on)
* ***Left click*** - performs whatever action is currently selected (show tile info, set tile, delete tile)
  

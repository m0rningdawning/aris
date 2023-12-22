# aris

Aris is a cross-platform, ASCII-styled Tetris clone made in Python for Windows and Linux.

![GitHub language count](https://img.shields.io/github/languages/count/m0rningdawning/aris)
![GitHub top language](https://img.shields.io/github/languages/top/m0rningdawning/aris) 
![GitHub last commit](https://img.shields.io/github/last-commit/m0rningdawning/aris)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Setup 

Before setting up the application, make sure ```Python 3``` is installed on your machine.

1. Clone the repository to your preferred location.
2. Navigate to the ```/release/aris``` directory.
3. Run ```pip install -e .``` or without ```-e``` flag to install a non editable script.  
**_NOTE:_** If during script installation you have received a ```PATH``` environmental variable warning, it is recommended to add the prompted path to the aforementioned variable to enable script execution from any directory.
4. - If ```PATH``` variable is **_not_** set, navigate to the prompted directory and type ```aris``` to run the game.
   - If ```PATH``` variable is set, type ```aris``` in the terminal of your choice and play!

Alternatively, you can run the game using Python without the need to install it:  
1. Navigate to the ```/release/aris/aris_pack``` or ```src``` directory.
2. Run ```Python3 .\aris.py``` on Windows or ```Python3 aris.py``` on Linux.

To uninstall the game run ```pip uninstall aris``` from your terminal.

## Preview

![image](https://github.com/m0rningdawning/aris/assets/102054245/e1e5cd33-dd24-4e18-abdf-54080f2160b7)

## Credits
Inspired by:  
- https://tetris.com/tetris-e60/

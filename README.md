
## Authors

* **Aniket Das** - *Development* - [s-dasa](https://github.com/s-dasa) - (aniket.das@scienceinfinity.org)
* **Deepayan Sanyal** - *Development* - [BoarCub](https://github.com/BoarCub)

# Precision Syringe Automator
The Precision Syringe Automator program creates a User Interface where communicaton with Hamilton's Precision Syringe Drive/4 is possible.
It allows the user to have full control of the pump's functionality (dispensing, retrieving, etc.), and can create routines that can be 
edited and loaded after the first use.

A packaged executable for Windows is available in the "dist" folder.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

1. You need Python 3.4 or higher. This is the programming language the project uses. This is available on the Python website at https://www.python.org/downloads/ if you don't already have it downloaded.

2. You need Kivy 1.11.0 or higher. Kivy is the Python graphics library used in this project for the user interface. This is available on the Kivy website at https://kivy.org/#download. Follow the installation intructions for your operating system.

3. You need the latest version of pySerial. pySerial allows the program to communicate with device using serial communication, in this case the pump. pySerial can be installed using pip with the following command:
```
pip install pyserial
```
4. You need a Python IDE of your choice. Make sure it is configured to the correct interpreter. Some of the IDEs used in this project were Thonny, Python IDLE and PyCharm.

### Installing

1. Clone this GitHub repository onto your computer.

2. Navigate to the clone repository.

3. Open the main.py file inside the Programs folder with your Python IDE.

4. Press the run button, and the program should run.

5. Edit any of the files in that folder (except .ttf files) to change the code.

### Settings To Be Aware Of

* To connect to the pump, the program searches for the correct USB Device using VID (Vendor ID) and PID (Product ID). These properties are set by the USB Device manufacturer so that each product has a unique ID. You can change the VID and PID of the device to connect to by opening the ```DistributionDatabase``` file inside the ```Databases``` folder and changing the numbers corresponding to each. By default, the VID and PID are ```1659``` and ```8963``` respectively. Make sure to change these properties if you're using a different USB connector than the one originally used.

* Make sure the DIP Switches on the back of the pump are set to the following:
```
Switch 1: Off
Switch 2: Off
Switch 3: Off
Switch 4: Off
Switch 5: On
Switch 6: On
Switch 7: On
Switch 8: On
```

* Make sure the Address Switch on the back of the pump is set to 0

## Deployment

### Deploying to Windows

Make sure the requirements are installed:
```
Latest Kivy (installed as described in Installation on Windows).
PyInstaller 3.1+ (pip install --upgrade pyinstaller).
```

1. Open your command line shell and ensure that python is on the path (i.e. python works).

2. Create a folder into which the packaged app will be created. For example, create a PrecisionSyringeAutomator folder and change to that directory with e.g. cd PrecisionSyringePump. Then type:
```
python -m PyInstaller --name PrecisionSyringePump INSERT_REPOSITORY_PATH\Program\main.py
```

3. The spec file will be PrecisionSyringeAutomator.spec located in PrecisionSyringeAutomator. Now we need to edit the spec file to add the dependencies hooks to correctly build the exe. Open the spec file with your favorite editor and add these lines at the beginning of the spec (assuming sdl2 is used, the default now):
```
from kivy_deps import sdl2, glew
```

To add the dependencies, before the first keyword argument in COLLECT add a Tree object for every path of the dependencies. E.g. *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)] so it’ll look something like:
```
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='touchtracer')
```

4. Now we need to make sure hidden dependencies are imported. Add a list containing the directory to the win32timezone file as follows:
```
my_hidden_modules = [( 'C:\\Users\\<username>\\AppData\\Local\\Programs\\Python\\<Python Version>\\Lib\\site-packages\\win32\\lib\\win32timezone.py', '.' )]
```

In ```a = Analysis```: change ```datas=[]``` to ```datas=my_hidden_modules```

5. Now we build the spec file in the PrecisionSyringePump folder with:
```
python -m PyInstaller PrecisionSyringePump.spec
```

6. Finally we have to include the other required folders/files with our program. There are two steps to this:

    a. Copy the Tasks and Databases folders from the Project Folder to the dist folder inside of the PrecisionSyringePump folder you    created
  
    b. Copy the Interface.kv and Corbel.ttf files from ```ProjectFolder\Programs``` to ```PrecisionSyringeAutomator\dist\PrecisionSyringeAutomator```
 
7. There is an executable inside ```dist\PrecisionSyringeAutomator``` called PrecisionSyringeAutomator which will run the program.




## License

All rights are reserved to InBios International

## Acknowledgments

* MIT's Kivy Documention https://kivy.org/doc/stable/

# Precision Syringe Automator

Dictionary in File Format: 
{1: ["Retrieve", [Input, Volume, Speed]], 2: ["Dispense", [Output, Volume, Speed]], 3: ["Recycle", [Output, Volume, Speed, Time, Bypass]], 4: ["Back-and-Forth", [Output, Volume, Speed, Time]]}


The Precision Syringe Automator program creates a User Interface where communicaton with Hamilton's Precision Syringe Drive/4 is possible.
It allows the user to have full control of the pump's functionality (dispensing, retrieving, etc.), and can create routines that can be 
edited and loaded after the first use.

To run program, run main.py

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
The .exe file
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

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
python -m PyInstaller --name PrecisionSyringePump examples-path\New_Project\Program\main.py
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
 
7. There is an executable inside ```dist\PrecisionSyringeAutomator``` called PrecisionSyringeAutomator that will run the program.

## Built With

* [Kivy 1.11.0](https://kivy.org/#changelog - User Interface Development
* [Python 3.7.4](https://https://www.python.org/downloads/release/python-374//) - Programming Language

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


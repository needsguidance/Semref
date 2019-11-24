# Semref: A Microprocessor Simulator

[![codecov](https://codecov.io/gh/needsguidance/Semref/branch/master/graph/badge.svg)](https://codecov.io/gh/needsguidance/Semref)

Semref is an application that serves as a simulator of a microprocessor. It simulates a variety of instructions and gives the user the choice of loading a set of instructions and either running them one by one or all at once. The simulator then shows the changes in memory and registers. The application also shows several different I/O modules, each one displaying or affecting the content of a specified memory address.

## Table of Contents 

* [Technologies](#Technologies)
* [Installation](#Installation) 
* [Microprocessor Specifications](#Microprocessor-Specifications) 
* [I/O Modules](#IO-Modules)
* [The User Interface](#The-User-Interface)
* [License](#License)
* [Authors and Acknowledgement](#Authors-and-Acknowledgement) 

## Technologies 

* [Python 2.7 - 3.5 - 3.6 - 3.7](https://www.python.org/downloads/release/python-374/) - interpreted, high-level, general-purpose programming language 
* [Kivy](https://kivy.org/#home) - a free and open source Python library for developing apps and other multitouch application software with a natural user interface. 
* [KivyMD](https://github.com/HeaTTheatR/KivyMD) - a collection of Material Design compliant widgets for use with Kivy, a framework for cross-platform, touch-enabled graphical applications. 

**NOTE:** The Kivy toolbox is not compatible with Python version 3.8. Thus, the application will not run with this version. Please ensure that the Python version being used is one specified above. 

## Installation 

As seen by the [Technologies](#Technologies) section shown above, the application depends on open-source, external Python libraries; Kivy and KivyMD are tools used to design the user interface of the application. To facilitate the installation process, an executable file called install.py was created. When this file is executed, every dependency needed by the program will be installed. To ensure that the versions used do not conflict with any versions already installed by the user, the creation of a virtual environment for the use of this application is recommended. This tutorial will serve as a guide to create a virtual environment, install the dependencies and run the program. The tutorial will assume that the user has already installed Python (version 3.6 or later).

### Step 1 - Creating a virtual environment 

As mentioned before, a virtual environment is recommended for the use of this application. To create a virtual environment, the command line can be used (if using an IDE such as PyCharm, the Command line is found on the **Terminal** section of the interface). 

First, the user must make sure that they have the **virtualenv** package installed in Python; this package manages virtual environment creation within Python. To install the **virtualenv** package, the user must run the following: 

```Shell
python -m pip install virtualenv
```

Now that the package is installed, the user can now create virtual environment. To create a virtual environment called **venv**, the user would have to run the following: 

```Shell
python -m virtualenv venv
``` 

It is important to note that **after creating the virtual environment, the virtual environment must be activated each time a new terminal is started**. The command used to activate the recently created **venv** is the following: 

* Windows 
 ```Shell
venv\Scripts\activate
``` 

* MacOS/Ubuntu
 ```Shell
source venv/bin/activate
```  
 
### Step 2 - Installing Dependencies 

As stated before, the GUI for the microprocessor simulator uses items from a third-party app development toolbox called Kivy. Therefore, in order to successfully run the application made, this toolbox must be installed into the computer. This would involve utilizing the pip install command in the command line, used for installing packages. Before installing the actual Kivy toolbox, one must install its dependencies. To simplify the installation process and avoid having to execute a significant amount of installation commands, the install.py file was created. By executing this file, all of the dependencies needed to run the microprocessor simulator (including Kivy and KivyMD) will be installed. In other words, the only thing needed to have all the dependencies installed is to run the install.py file included in the project folder. To execute this file, run the following: 

```Shell
python install.py
``` 

### Step 3 - Executing the Program

Finally, the only step remaining is to run the program. This is done by running the main file: 

```Shell
python main.py
```  

The program should now be running smoothly on the computer. 

## Microprocessor Specifications 

The microprocessor that is being simulated has a 4 KB memory. The instructions are always stored in even-numbered memory addresses, while the data can be stored anywhere. Instructions occupy 16 bits, while other data occupies 8. The microprocessor has eight 8-bit registers, from R0 to R7. R0 is always zero, and R1 will serve as accumulator for certain instructions. In addition to these registers, the microprocessor also counts with an 11-bit Program Counter, a 12-bit Stack Pointer, and a 16-bit Instruction Register. 

## I/O Modules 

The microprocessor simulator counts with several I/O modules in its interface. Each one displays the content of a specified memory address, with the exception of one module that changes the content of the specified port. The memory locations utilized as ports can be changed to any available address. Below is I/O Module explained.  

### Traffic Light 

The traffic light module consists of two traffic light widgets. This feature reads the content found on the port specified by the user. The first six bits will represent the six lights on the two traffic lights in top-to-bottom order, with the left traffic light representing the first three bits and the right traffic light showing the other three. A one on the bit would represent an activated light, whereas a zero value would show a turned off light. For example, the six bits "100100" would show the two red lights of each traffic light turned on. The final two bits decide whether or not the content shown by the activated traffic lights should be intermittent. If the two least significant bits are both 1, then the lights will be blinking. To use the past example, the bits "10010011" would show the two red lights blinking. 

### Seven Segment Display 

The 7-segment display shows two digits with a seven-segment configuration. This feature utilizes the content of one 8-bit memory address specified by the user. The 7 most significant bits represent the seven segments of a digit: a,b,c,d,e,f & g, respectively. For example, the seven bits "1000101" would show the segments a, e & g. The remaining, least significant bit decides which one of the two digits will display the segments activated by the bits: A zero would show the seven segments on the left digit, while a one would show the seven segments on the right digit. Thus, the byte "10001011" would show the segments a, e & g turned on for the right-side digit.  

### ASCII Grid 

The ASCII Grid is the only I/O module that needs more than one memory address. Eight contiguous memory addresses are reserved for this I/O. The ASCII Grid consists of eight squares, each one representing one memory address. Each square on the grid will display the ASCII character that is represented by the eight bits shown in that specific memory address. For example, the memory content "10000001" would show the letter 'A' in the square corresponding to that memory address.

### Hex Keyboard 

The hex keyboard is the only I/O module that modifies a memory content in the specified port instead of just displaying its content in some way. The Hex Keyboard consists of 16 buttons, each representing hexadecimal digits 0-F. When a key is pressed, the memory content of the address connected to that port will now change its value to that hexadecimal digit. 

## The User Interface

The user interface displays the following: 

### Top of the Window

At the top of the window, there are several buttons. The vertical ellipsis in the top left corner expands a menu that contains the following choices:

  - **Load File**: This option serves as a file explorer, enabling the user to load assembler instructions in a .obj format. 
  - **Configure Traffic Light Port**: The user can change the memory address shown by the traffic light I/O. The traffic light I/O will display the contents of the memory address specified by the user.
  - **Configure 7 Segment Display**: The user can change the memory address shown by the 7 Segment Display I/O. The seven segment display will show the contents of the memory address specified by the user. 
  - **Configure ASCII Table Port**: The user can change the memory address shown by the ASCII Grid. Since each block in the 8-digit grid represents a complete memory address, this port automatically reserves 8 memory positions. The user selects the first memory address to be shown; the remaining seven will be the seven addresses immediately following the one selected by the user. 
  - **Configure Hex Keyboard Port**: The user can change the memory address affected by the Hex Keyboard. The user's input in the keyboard directly controls the memory address specified by the user. 

**NOTE**: Each I/O module must have its own unique port; that is, two I/O modules cannot share the same memory address as their port. 

The rest of the buttons that are displayed in the green section of the top of the window are: 

- **Run** - Runs all of the instructions that have been loaded. 
- **Debug** - A step-by-step method of running through instructions loaded. Each button press executes one instruction. 
- **Clear** - Clears the simulator and removes the .obj file that is currently being read. 
- **Save File** - Saves the current contents of the simulation as is. 
- **Hex Keyboard** - Triggers the hex keyboard to be displayed as a pop-up on the screen in a separate window. 

### Tables 

Three tables are visible immediately under the green buttons. The first table shows the contents of the eight registers, the program counter, the stack pointer, the Instruction Register and the conditional bit. The second table shows the disassembled instructions in the order that they're being executed. Thus, if the debug button is being used, the instructions will be made visible one by one with each press. The third table shows the content of the first 50 memory addresses. 

### I/O Modules 

With the exception of the hex keyboard, the I/O modules can be seen afterwards. This includes the ASCII Grid, 7-segment display and traffic lights, all explained above. 

### Editor

Finally, there is an editable text box that can be used to write down instructions for the assembler to execute. 

## License 
```
MIT License

Copyright (c) 2019 Semref

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Authors and Acknowledgement 
* **Noel Valentin** - [noelvalentin](https://github.com/noelvalentin)
* **Christian Pérez** -  [ChristianPerez34](https://github.com/ChristianPerez34)
* **Christian Torres** - [cfboy](https://github.com/cfboy)
* **Alejandro Reyes** - [alejoreyes96](https://github.com/alejoreyes96)

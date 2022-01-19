# Temperature_Controller-SW

With this program you can control the [Temperature Controller](https://github.com/norbertg1/Temperature_Controller-HW) hardware from computer through serial port. 
Also you can set the temperature in range with custom steps and time between.

## Packages you need:
``` 
pip install matplotlib
pip install tk
pip install pyserial
pip install crcmod
pip install pyautogui
pip install opencv_python
sudo apt-get install python3-pil python3-pil.imagetk
sudo apt-get install scrot
``` 
# Run 
Run with command ``` python3 TempControl.py ``` 
There is a nice graphical intuitive interface with comments.

# Make an executable file for Windows

You need a package: 

```pip install pyinstaller```

and run 

```pyinstaller --onefile TempControl.py```

# Comments

Files: ```start_button_img.py, start_button.png, pic2str.py``` are for controlling our custom made measurement device. Please ignore them also with checkbox "Control IVMaster".
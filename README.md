# Simple subtitle translator

A simple subtitle translator using python, tesseract and Google translate! 

## Installation

### if you are on windows 10 you have 2 options.

*Using the PyInstaller standalone:*

1. Download the Sub_translatorV3.zip file and unzip it. 

2. Open the folder and find the Sub_translatorV3 executable.  
![tutorial1](tutorial1.png) 

3. Click on it and it should start. (Note: when you open it for the first time you might get a security warning since windows doesn't know the contents of the executable)    
![tutorial2](tutorial2.png)

In that case simply click "more info", then click "run anyway".

*Using the source code:*
1. Download the source code file, Sub_translatorV3.py. Then download the Tesseract-OCR.zip file and unzip it.
2. Put them on the on the same directory.
3. (Make sure you have python and all modules imported installed on your machine.)  
4. Ready to go. 

### if you aren't using windows 10: 

*Using the source code:*
1. Download the source code file, Sub_translatorV3.py. Then download the Tesseract-OCR.zip file and unzip it.
2. Put them on the on the same directory.
3. (Make sure you have python and all modules imported installed on your machine.)  
4. Ready to go. 

(NOte that this software has been tested for windows 10. If you find an issue when using another platform let me know.)

## How to use

When opening the programm it will print the following information on how to effectively use it:  

 *Subtitle traslator V3  
 A simple tool built for translating subtitles in real time  
 Made by kkounal (https://github.com/kkounal)*  
 
*--------------------------------------*

*Overview of basic function:*

 *The translator consists of two windows.  
 One of the windows is used to mark the part of the screen one wishes to translate and is trasparent.*

* The other is used at first as a menu.  
 But after the button "Ready" has been pressed it acts as a container to display the translated text.*
 
*--------------------------------------*

 *Overview of how to effectively use the control buttons:*

 *Ready: Press to start tanslating.*

 *Test: Used to test proper function of programm.  
 Once pressed it will show importart steps in the image preproccesing and text recognision proccess.  
 They can be used to troubleshot problems. Prints identified subtitles in the console.*

 *Select custom target color: Color detection is used to seperate subtitle text from the background.  
 Usually subtitles are white so the default is also white.  
 If yours aren't you can press this button and play around with the sliders.  
 Aim for clear text on a black background with as little noise as possible for best results.  
 Then simply close the window or press esc. Combine with Test button to troubleshoot.*

 *Select custom display color: Opens a color picker dialog window where the user can choose the color   
 of the translated text. Default is a nice yellow, (#fcbe11).* 

 *Place windows: Just a shortcut for placing the windows. Made with fullscreen in mind.*
 
 *Change languages: Pressing will open a window with three textboxes for input and three buttons to confirm.    
 The first is for the target language for tesseract, the Optical Character Recognisition software this app built on.    
 The second and third are for google translate. Find supported languages here:  
 https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html  
 https://cloud.google.com/translate/docs/languages*

 *Save settings: Pressing will save all current settings to be used again when open the app.  
 These include the subtitle display color, target subtitle color and all language settings.*

 *Restore default: Restores default settings.*

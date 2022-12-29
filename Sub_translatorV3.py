import cv2
import mss
import numpy as np
import pytesseract
from pytesseract import Output
import threading
import tkinter as tk
from tkinter.colorchooser import askcolor
from deep_translator import GoogleTranslator
import ctypes
from pathlib import Path


ctypes.windll.user32.SetProcessDPIAware(1)  # to fix weird bug with mss , it also makes tkinter less blurry maybe
pytesseract.pytesseract.tesseract_cmd = r'%s\Tesseract-OCR\tesseract.exe' % Path(__file__).parent.absolute() # might want to change this if you are not on windows

start=False
text_to_show="no text"
color="#fcbe11"

upper_color=np.array([255,10,255])
lower_color=np.array([0,0,245]) 
custom_color_bool=0

lang_tesseract="eng"
lang_from_google="auto"
lang_to_google="el"



print(" Subtitle traslator V3 \n A simple tool built for translating subtitles in real time\n Made by kkounal (https://github.com/kkounal)\n--------------------------------------\n Overview of basic function:\n\n The translator consists of two windows.\n One of the windows is used to mark the part of the screen one wishes to translate and is trasparent.")
print("\n The other is used at first as a menu.\n But after the button \"Ready\" has been pressed it acts as a container to display the translated text.")
print("--------------------------------------\n Overview of how to effectively use the control buttons:")
print("\n Ready: Press to start tanslating.")
print("\n Test: Used to test proper function of programm.\n Once pressed it will show importart steps in the image preproccesing and text recognision proccess.\n They can be used to troubleshot problems. Prints identified subtitles in the console.")
print("\n Select custom target color: Color detection is used to seperate subtitle text from the background.\n Usually subtitles are white so the default is also white.\n If yours aren't you can press this button and play around with the sliders.")
print(" Aim for clear text on a black background with as little noise as possible for best results.\n Then simply close the window or press esc. Combine with Test button to troubleshoot.")
print("\n Select custom display color: Opens a color picker dialog window where the user can choose the color\n of the translated text. Default is a nice yellow, (#fcbe11).")
print("\n Place windows: Just a shortcut for placing the windows. Made with fullscreen in mind.")
print("\n Change languages: Pressing will open a window with three textboxes for input and three buttons to confirm.")
print("\n The first is for the target language for tesseract, the Optical Character Recognisition software this app built on.")
print("\n The second and third are for google translate. Find supported languages here: \n https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html \n https://cloud.google.com/translate/docs/languages")
print("\n Save settings: Pressing will save all current settings to be used again when open the app.\n These include the subtitle display color, target subtitle color and all language settings.\n")
print(" Restore default: Restores default settings.\n")

root = tk.Tk() #the window
root.title('Subtitle translator')
root.attributes('-topmost',True)
root.geometry('1000x150')

w2=tk.Toplevel()
w2.title('Place above text')
w2.attributes('-topmost',True)
w2.geometry('1000x100+10+10')
w2.attributes('-alpha',0.7)


def load_saved_data():
    global color
    global lang_tesseract
    global lang_from_google
    global lang_to_google
    global upper_color
    global lower_color
    global custom_color_bool
    counter=0
    path_to_file = 'saved_settings.txt'
    path = Path(path_to_file)

    if path.is_file():
        with open('saved_settings.txt','r',encoding='utf8') as f:
            for line in f:
                currentline = line.strip().split("~")
                for word in currentline:
                    counter+=1
                    if counter==1:
                        color=word
                    elif counter==2:
                        lang_tesseract=word
                    elif counter==3:
                        lang_from_google=word
                    elif counter==4:
                        lang_to_google=word
                    elif counter==5:
                        upper_color=np.fromstring(word[1:-1], dtype=int, sep=' ')
                    elif counter==6:
                        lower_color=np.fromstring(word[1:-1], dtype=int, sep=' ')
                    elif counter==7:
                        custom_color_bool=int(word)
                    else:
                        pass
        f.close()                         
                
        
load_saved_data()


def write_saved_data():
    global color
    global lang_tesseract
    global lang_from_google
    global lang_to_google
    global upper_color
    global lower_color
    global custom_color_bool
    words=[color,lang_tesseract,lang_from_google,lang_to_google,upper_color,lower_color,custom_color_bool]
    with open('saved_settings.txt','w',encoding='utf8') as f:
        for word in words:
            f.write(str(word))
            f.write("~")
        f.close()

def restore_default_saved_data():
    global color
    global lang_tesseract
    global lang_from_google
    global lang_to_google
    global upper_color
    global lower_color
    global custom_color_bool

    color="#fcbe11"
    upper_color=np.array([255,10,255])
    lower_color=np.array([0,0,245])  
    custom_color_bool=0
    lang_tesseract="eng"
    lang_from_google="auto"
    lang_to_google="el"
    
    words=[color,lang_tesseract,lang_from_google,lang_to_google,upper_color,lower_color,custom_color_bool]
    with open('saved_settings.txt','w',encoding='utf8') as f:
        for word in words:
            f.write(str(word))
            f.write("~")
        f.close()        



def window_place():
    # weird bug with mss changes windows when first called 
    with mss.mss() as sct:
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen
        root.geometry('%dx%d+%d+%d' % (ws-20, (hs/3)-20, 0, 10))
        w2.geometry('%dx%d+%d+%d' % (ws-20, (hs/3)+0.04*hs, 0,((2*hs)/3)-0.07*hs))

def close_main_win():
   root.destroy() 


def nothing(x):
    pass

def find_color_window(mon):

    global upper_color
    global lower_color
    global custom_color_bool
    root.withdraw()
    cv2.destroyAllWindows()
    w2.attributes('-alpha',0)
    img = np.asarray(mss.mss().grab(mon))
    w2.attributes('-alpha',0.7)
    w2.withdraw()
    
    
    
    # Create a window
    cv2.namedWindow('Find color',cv2.WINDOW_AUTOSIZE)
    


    # Create trackbars for color change
    # Hue is from 0-179 for Opencv
    cv2.createTrackbar('HMin', 'Find color', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'Find color', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'Find color', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'Find color', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'Find color', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'Find color', 0, 255, nothing)

    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMax', 'Find color', 179)
    cv2.setTrackbarPos('SMax', 'Find color', 255)
    cv2.setTrackbarPos('VMax', 'Find color', 255)

    # Initialize HSV min/max values
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    while(1):
        # Get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin', 'Find color')
        sMin = cv2.getTrackbarPos('SMin', 'Find color')
        vMin = cv2.getTrackbarPos('VMin', 'Find color')
        hMax = cv2.getTrackbarPos('HMax', 'Find color')
        sMax = cv2.getTrackbarPos('SMax', 'Find color')
        vMax = cv2.getTrackbarPos('VMax', 'Find color')

        # Set minimum and maximum HSV values to display
        lower_color = np.array([hMin, sMin, vMin])
        upper_color = np.array([hMax, sMax, vMax])

    

        # Convert to HSV format and color threshold
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        result = cv2.bitwise_and(img, img, mask=mask)

        # See if there is a change in HSV value
        if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display result image
        cv2.imshow('Find color', result)
        k = cv2.waitKey(1) & 0xFF  # Capture the code of the pressed key.
        # Stop the loop when the user clicks on GUI close button [x].
        if not cv2.getWindowProperty('Find color', cv2.WND_PROP_VISIBLE):
            print("Color of target subtitles picked:  ")
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            break
        if k == 27:  # Key code for ESC
            break 

    custom_color_bool=1
    root.deiconify()
    w2.deiconify()
    cv2.destroyAllWindows()


def change_languages():
    global textBox
    global textBox2
    global textBox3
    
    lang_window = tk.Toplevel(root)
    lang_window.title("Change languages")
    lang_window.geometry("800x300")
    label = tk.Label(lang_window,font=("Arial Black", 10),text="Select language to translate from (for tesseract, default is english \"eng\")")
    label.pack()
    textBox=tk.Text(lang_window, height=1, width=10)
    textBox.pack()
    buttonCommit=tk.Button(lang_window, height=1, width=10, text="Select", command=lambda: retrieve_input(1))
    buttonCommit.pack()

    label2 = tk.Label(lang_window,font=("Arial Black", 10),text="Select language to translate from (for Google translate, default is automatic \"auto\")")
    label2.pack()
    textBox2=tk.Text(lang_window, height=1, width=10)
    textBox2.pack()
    buttonCommit2=tk.Button(lang_window, height=1, width=10, text="Select", command=lambda: retrieve_input(2))
    buttonCommit2.pack()

    label2 = tk.Label(lang_window,font=("Arial Black", 10),text="Select language to translate to (for Google translate, default is greek \"el\")")
    label2.pack()
    textBox3=tk.Text(lang_window, height=1, width=10)
    textBox3.pack()
    buttonCommit3=tk.Button(lang_window, height=1, width=10, text="Select", command=lambda: retrieve_input(3))
    buttonCommit3.pack()
   
def retrieve_input(num):
    global textBox
    global textBox2
    global textBox3
    global lang_tesseract
    global lang_from_google
    global lang_to_google
    
    if num==1:
        inputValue=textBox.get("1.0","end-1c")
        lang_tesseract=inputValue
        print("Selected language to translate from, (for tesseract): %s" % inputValue)
    elif num==2:
        inputValue=textBox2.get("1.0","end-1c")
        lang_from_google=inputValue
        print("Selected language to translate from, (for Google translate): %s" % inputValue)
    else:
        inputValue=textBox3.get("1.0","end-1c")
        lang_to_google=inputValue
        print("Selected language to translate to, (for Google translate): %s" % inputValue)


def white_only(img):
    global upper_color
    global lower_color
    
    if custom_color_bool==False:
        # define range of white color in HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        sensitivity = 10
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])
        # Threshold the HSV image to get only white colors
        mask = cv2.inRange(hsv, lower_white, upper_white)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(img,img, mask= mask)    
        kernel = np.ones((3, 3), np.uint8)
        img = cv2.dilate(res, kernel, iterations = 1)
        #invert
        img = (255-img)
    else:
        # define range of white color in HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Threshold the HSV image to get only white colors
        mask = cv2.inRange(hsv, lower_color, upper_color)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(img,img, mask= mask)    
        kernel = np.ones((3, 3), np.uint8)
        img = cv2.dilate(res, kernel, iterations = 1)

        img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _ , img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
        img=cv2.merge([img,img,img])
        
                
    return img

def find_text(img):
    
    img=white_only(img)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255,255,255), -1)
    img2=img.copy()
    cv2.imshow("Subtitles, isolated from the background", img2)
    return img

def crop_using_white(img,img_to_crop):
    img=255-img
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17,17))
    dilate = cv2.dilate(img, vertical_kernel, iterations=2)
    contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea,default=None)
    if c is None:
        return img_to_crop
    else:    
        x,y,w,h = cv2.boundingRect(c)
        h=20+h
        w=20+w
        x=x-10
        y=y-10
        img_to_crop = img_to_crop[y:y+h, x:x+w]
        
        return img_to_crop 

    
#ROI = image[y1:y2, x1:x2]
#-------------------------------------------
#|                                         | 
#|    (x1, y1)                             |
#|      ------------------------           |
#|      |                      |           |
#|      |                      |           | 
#|      |         ROI          |           |  
#|      | (Region of interest) |           |   
#|      |                      |           |   
#|      |                      |           |       
#|      ------------------------           |   
#|                           (x2, y2)      |    
#|                                         |             
#|                                         |             
#|                                         |             
#-------------------------------------------

    
def test():
    global text_to_show
    
    global upper_color
    global lower_color

    global lang_tesseract
    global lang_from_google
    global lang_to_google
    
    window_x, window_y = w2.winfo_rootx(), w2.winfo_rooty()
    window_width,window_height = w2.winfo_width(), w2.winfo_height()
    mon = {'top': window_y, 'left': window_x, 'width': window_width, 'height': window_height}
    
    
    w2.attributes('-alpha',0)
    
    img = np.asarray(mss.mss().grab(mon))

    img2=img.copy()

    img2=find_text(img2)
    

    img=crop_using_white(img2,img)
    cv2.imshow("Image cropped to only region with subtitles", img)

    #Convert to grayscale and equalise
    img=white_only(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=cv2.equalizeHist(img)


    #Show results

    c = pytesseract.image_to_string(img, config='--psm 6 --oem 3 -c tessedit_char_blacklist=:@{[}]<*>^§~®|', lang=lang_tesseract)
    text_to_show=c
    print("output is: ")
    print(text_to_show)

    d = pytesseract.image_to_data(img, config='--psm 6 --oem 3 -c tessedit_char_blacklist=:@{[}]<*>^§~®|', lang=lang_tesseract, output_type=Output.DICT)
    img=cv2.merge([img,img,img])
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (200, 0, 200), 2)

    img3=img.copy()
    cv2.imshow('OCR result', img3)


    w2.attributes('-alpha',0.7)

    
    


def go():
    global start
    global color
    global window_x, window_y
    global window_width,window_height 
    
    w2.attributes('-alpha',0)
    

    color_button.after(1, color_button.destroy)
    B.after(1, B.destroy)
    B2.after(1, B2.destroy)
    B3.after(1, B3.destroy)
    B4.after(1, B4.destroy)
    B5.after(1, B5.destroy)
    B6.after(1, B6.destroy)
    B7.after(1, B7.destroy)
    
    cv2.destroyAllWindows()
    root.wm_attributes('-transparentcolor','black')
    root.overrideredirect(1)
        
    window_x, window_y = w2.winfo_rootx(), w2.winfo_rooty()
    window_width,window_height = w2.winfo_width(), w2.winfo_height()

    root_height=root.winfo_height()
    root_width=root.winfo_width()
    label.pack()

    letter_size=int((root_height*root_height)/1000)
    if letter_size>35:
        letter_size=35
    label.config(font = ("Arial Black", letter_size))


    label.config(padx=50,pady=30,background="black",foreground=color,width=root_width-20,height=root_height-20,wraplength=root_width-20)

    start=True
    manager()


def change_color():
    global color
    color = askcolor(color="#fcbe11", title="Tkinter Color Chooser")
    color=color[1]
    

#two differnt ones to minimize if statements for better speed
def do_the_thing_white(mon,lang_tesseract,lang_from_google,lang_to_google):
    global text_to_show
    
    original_img = np.asarray(mss.mss().grab(mon))
    img=original_img.copy()

    #find_text(img)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,245])
    upper_white = np.array([255,10,255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    res = cv2.bitwise_and(img,img, mask= mask)    
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(res, kernel, iterations = 1)
    img = (255-img)
    

    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255,255,255), -1)
    
    
    
    #crop_using_white(img,original_img)
    

    img=255-img
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (19,19))
    dilate = cv2.dilate(img, vertical_kernel, iterations=2)
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea, default=None)
    if c is not None and img.size > 0:    
        x,y,w,h = cv2.boundingRect(c)
        h=20+h
        w=20+w
        x=x-10
        y=y-10
        original_img = original_img[y:y+h, x:x+w]    
        img=original_img
        
        if img.size>0:
            
            
            
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_white, upper_white)
            res = cv2.bitwise_and(img,img, mask= mask)    
            kernel = np.ones((3, 3), np.uint8)
            img = cv2.dilate(res, kernel, iterations = 1)
            #invert
            img = (255-img)

                
               
            #Convert to grayscale and equalise
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img=cv2.equalizeHist(img)

            text = pytesseract.image_to_string(img, config='--psm 6 --oem 3 -c tessedit_char_blacklist=:@{[}]<*>^§~®|', lang=lang_tesseract)
            text_to_show = GoogleTranslator(source=lang_from_google, target=lang_to_google).translate(text)
        else:
            text_to_show=""    
    else:

        text_to_show=""
                    
def do_the_thing_color(mon,upper_color,lower_color,lang_tesseract,lang_from_google,lang_to_google):
    global text_to_show

    original_img = np.asarray(mss.mss().grab(mon))
    img=original_img.copy()


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    res = cv2.bitwise_and(img,img, mask= mask)    
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(res, kernel, iterations = 1)

    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret ,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    img=cv2.merge([img,img,img])

    img=255-img
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (19,19))
    dilate = cv2.dilate(img, vertical_kernel, iterations=2)
    dilate=cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea, default=None)
    if c is not None and img.size > 0:    
        x,y,w,h = cv2.boundingRect(c)
        h=20+h
        w=20+w
        x=x-10
        y=y-10
        original_img = original_img[y:y+h, x:x+w]    
        img=original_img
        
        if img.size>0:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_color, upper_color)
            res = cv2.bitwise_and(img,img, mask= mask)    
            kernel = np.ones((3, 3), np.uint8)
            img = cv2.dilate(res, kernel, iterations = 1)
            img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret ,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
            img=cv2.merge([img,img,img])

            #Convert to grayscale and equalise
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img=cv2.equalizeHist(img)

            text = pytesseract.image_to_string(img, config='--psm 6 --oem 3 -c tessedit_char_blacklist=:@{[}]<*>^§~®|', lang=lang_tesseract)
            text_to_show = GoogleTranslator(source=lang_from_google, target=lang_to_google).translate(text)
        else:
            text_to_show=""    
    else:

        text_to_show=""
        


def my_mainloop_white():
    global text_to_show
    global window_x, window_y
    global window_width,window_height
    global lang_tesseract
    global lang_from_google
    global lang_to_google 
        
    threading.Thread(target=do_the_thing_white({'top': window_y, 'left': window_x, 'width': window_width, 'height': window_height},lang_tesseract,lang_from_google,lang_to_google)).start()        
    label.config(text=text_to_show)        
    root.after(5,my_mainloop_white)  # run again after 5ms (0.005s)

def my_mainloop_color():
    global text_to_show
    global window_x, window_y
    global window_width,window_height 
    global upper_color
    global lower_color
    global lang_tesseract
    global lang_from_google
    global lang_to_google
        
    threading.Thread(target=do_the_thing_color({'top': window_y, 'left': window_x, 'width': window_width, 'height': window_height},upper_color,lower_color,lang_tesseract,lang_from_google,lang_to_google)).start()        
    label.config(text=text_to_show)
    root.after(5,my_mainloop_color)    

def manager():
    global custom_color_bool
    if custom_color_bool==False:        
        root.after(1, my_mainloop_white)
    else:
        root.after(1, my_mainloop_color)



label = tk.Label(root,font=("Arial Black", 10))

B = tk.Button(root,text ="Ready", command = go)
B.pack(side='left', fill='x', expand=True)

B2 = tk.Button(root,text ="Test", command = test)
B2.pack(side='left',fill='x', expand=True)

color_button=tk.Button(root,text='Select custom target color',command=lambda: find_color_window({'top': w2.winfo_rooty(), 'left': w2.winfo_rootx(), 'width': w2.winfo_width(), 'height': w2.winfo_height()}))
color_button.pack(side='left',fill='x', expand=True)

B3 = tk.Button(root,text ="Select custom display color", command = change_color)
B3.pack(side='left',fill='x', expand=True)

B4 = tk.Button(root,text ="Place windows", command = window_place)
B4.pack(side='left',fill='x', expand=True) 

B5 = tk.Button(root,text ="Change languages", command = change_languages)
B5.pack(side='left',fill='x', expand=True) 

B6 = tk.Button(root,text ="Save settings", command = write_saved_data)
B6.pack(side='left',fill='x', expand=True)

B7 = tk.Button(root,text ="Restore default", command = restore_default_saved_data)
B7.pack(side='left',fill='x', expand=True)





w2.protocol("WM_DELETE_WINDOW",lambda: close_main_win()) 
       
w2.mainloop()
    
   
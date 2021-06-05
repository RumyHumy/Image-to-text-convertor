import os, random, math
from os import path
from PIL import Image as PILImage
import clipboard
from tkinter import *
from tkinter import filedialog
defaultPlette='░▒▓█' # Default symbols plette
defaultFont = 'Calibri 12' # Font for GUI buttons
def ExtractImage():
    filePath = filedialog.askopenfilename(filetypes=(('Image files', '*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.ico'), ("All files", "*.*"))) # Get user's file
    return filePath # Return it
def Click(): # "Image to text" function
    textState.delete(1.0, END) # Clear all text
    newsize = [0]*2 # Define new size array
    imagePath = ExtractImage() # Get the image path
    image = PILImage.open(imagePath) # Open image
    textState.insert(END, 'Enter the size!'+'\nOriginal size: '+str(image.size[0])+'x'+str(image.size[1])) # No size found error
    newsize[0] = int(lineWidth.get()) # Set new image sizes
    newsize[1] = int(lineHeight.get())
    oldSize = image.size # Memorising the size
    textState.delete(1.0, END) # Clear error text
    image = image.resize(newsize) # Resize the image
    W, H = image.size # Get image size
    map = image.load() # Load pixels to work with
    P = lineCustom.get() # Get custom plette line
    if len(P) <= 0: P = defaultPlette # If user didn't enter custom plette, then set it to default
    ditOn = 1 # Define and set enabled dithering option
    ditMap = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]] # Dithering map
    textPicture='' # Clear and define picture string
    for y in range(H): # For every pixel in the image
        for x in range(W):
            pix=map[x, y] # Get current pixel colors (RGB)
            val=(pix[0]+pix[1]+pix[2])/255/3 # Get the medium color
            color = val*(len(P)-0.5)# Get symbol color order
            stepValue = color-math.floor(color) # Get the transition power
            if ditOn: addCorrector = stepValue>ditMap[x%4][y%4]/16 # If dithering is on, then dither
            else: addCorrector = round(stepValue) # Else round
            textPicture+=P[int(max(min(color+addCorrector,len(P)-1),0))] # Add symbol
        textPicture+=chr(10) # Separate
    clipboard.copy(textPicture) # Copying the result
    textState.insert(END,'Copied!\n'+'Old size: '+str(oldSize[0])+'x'+str(oldSize[1])+'\nNew size: '+str(image.size[0])+'x'+str(image.size[1])+'\nPath: '+imagePath+'\n'+textPicture)
    image.close()
window = Tk() # Tkinter define
window.title("ImageToText-er by RumyHumy") # Set window title
if path.isfile('icon/exe_and_window_icon.ico'): window.iconbitmap('icon/exe_and_window_icon.ico')
window.geometry("800x800") # Set window size

labWidth = Label(window, text='\n*Width: ', width=75, font=defaultFont) # Width caption
labWidth.pack()
lineWidth = Entry(window, width=25, font=defaultFont) # Width line
lineWidth.pack()
labHeight = Label(window, text='\n*Height: ', width=75, font=defaultFont) # Height caption
labHeight.pack()
lineHeight = Entry(window, width=25, font=defaultFont) # Height line
lineHeight.pack()
labCustom = Label(window, text='\nCustom plette (example: \'░▒▓█\', \'.-=#@\', \'781 782\'): ', font=defaultFont) # Custom caption
labCustom.pack()
lineCustom = Entry(window, width=75, font=defaultFont) # Custom line
lineCustom.pack()
butResult = Button(window, text="Print", command=Click, font=defaultFont) # Result button
butResult.pack()

wScroll = Scrollbar(window, orient='horizontal') # Set scrollbars for text
wScroll.pack(side='bottom', fill='x')
hScroll = Scrollbar(window, orient='vertical')
hScroll.pack(side='right', fill='y')
textState = Text(window, width=100, height=30, font='Courier_New 8', wrap=NONE, xscrollcommand=wScroll.set, yscrollcommand=hScroll.set) # Text field
textState.insert(END, '...')
textState.pack()
wScroll.config(command=textState.xview) # Set scroll commands
hScroll.config(command=textState.yview)
while 1: # Mainloopa
    window.update_idletasks()
    window.update()
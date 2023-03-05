import tkinter as tk
import cv2
from PIL import ImageTk,Image 
from tkinter.filedialog import askopenfilename
import numpy as np

window = tk.Tk()
window.title('ImEd')
window.geometry('800x500')
window.configure(bg = '#282923')

window.rowconfigure(1, weight = 1)
window.columnconfigure(0, weight = 1)

imageRaw = []
check = False
isGray = False


def openImage():
	global path
	path = askopenfilename(
		filetypes=[("All Files", "*.*")]
	)
	global check
	global isGray

	isGray = False
	check = False

	getInitialImage()
	imageBox()

def save():
	imageRaw = collect('',0)
	if imageRaw == []:
		label = tk.Label(window, text = "First select an image!")
		label.grid(row = 1, column = 0)
	if isGray == False:
		b,g,r = cv2.split(imageRaw)
		imageRaw = cv2.merge((r,g,b))
	cv2.imwrite("newimage.jpg", imageRaw)

def getInitialImage():
	global image
	imageRaw = cv2.imread(path)

	scale_percent = 100

	if isGray == False:
		h,w,c = imageRaw.shape
	else:
		h,w = imageRaw.shape

	if w >= 2100 or h >= 2100:
		scale_percent = 15
	elif w > 700 or h > 700 and w < 2000 and h < 2000:
		scale_percent = 40
	width = int(imageRaw.shape[1] * scale_percent / 100)
	height = int(imageRaw.shape[0] * scale_percent / 100)
	dsize = (width, height)
	imageRaw = cv2.resize(imageRaw, dsize)

	faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
	faces = faceCascade.detectMultiScale(
    	imageRaw,
    	scaleFactor=1.3,
    	minNeighbors=3,
    	minSize=(30, 30)
	)
	for (x, y, w, h) in faces:
		cv2.rectangle(imageRaw, (x, y), (x + w, y + h), (0, 255, 0), 2)

	b,g,r = cv2.split(imageRaw)
	imageRaw = cv2.merge((r,g,b))
	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	collect(imageRaw,1)
	__faces(len(faces),1)



def menuBar():
	frm_oprionsButtons = tk.Frame(window, relief = tk.RAISED, bd=2, bg = '#282923')

	btn_open = tk.Button(frm_oprionsButtons, text = 'Open', relief = tk.RAISED,bg = '#42433e', fg = "white", command = openImage)
	btn_save = tk.Button(frm_oprionsButtons, text = 'Save', relief = tk.RAISED,bg = '#42433e', fg = "white", command = save)

	btn_open.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)
	btn_save.grid(row = 0, column = 1, sticky = 'w', padx = 5, pady = 5)

	frm_oprionsButtons.grid(row = 0, column = 0, sticky = 'new')

def modificationBar():
	frm_modifications = tk.Frame(window, relief = tk.RAISED, bd=1, bg = '#282923')

	btn1 = tk.Button(frm_modifications, text = 'Crop', relief = tk.FLAT, bg = '#42433e', fg = "white", command = crop)
	btn2 = tk.Button(frm_modifications, text = 'Mirror', relief = tk.FLAT, bg = '#42433e', fg = "white" , command = mirror)
	btn3 = tk.Button(frm_modifications, text = 'Rotate 90', relief = tk.FLAT, bg = '#42433e', fg = "white" , command = rotate)
	btn_toGray = tk.Button(frm_modifications, text = 'Grayscale', relief = tk.FLAT, bg = '#42433e', fg = "white", command = toGray)
	btn_negativ = tk.Button(frm_modifications, text = 'Negativ', relief = tk.FLAT, bg = '#42433e', fg = "white" , command = negativ)
	btn_red = tk.Button(frm_modifications, relief = tk.FLAT, bg = 'red', command = red)
	btn_green = tk.Button(frm_modifications, relief = tk.FLAT, bg = 'green', command = green)
	btn_blue = tk.Button(frm_modifications, relief = tk.FLAT, bg = 'blue', command = blue)
	
	btn1.grid(row = 0, column = 0, sticky = 'new', padx = 5, pady = 5,)
	btn2.grid(row = 1, column = 0, sticky = 'new', padx = 5, pady = 5,)
	btn3.grid(row = 2, column = 0, sticky = 'new', padx = 5, pady = 5,)
	btn_toGray.grid(row = 3, column = 0, sticky = 'new', padx = 5, pady = 5,)
	btn_negativ.grid(row = 4, column = 0, sticky = 'new', padx = 5, pady = 5,)
	btn_red.grid(row = 5, column = 0, sticky = 'new', padx = 5, pady = 5,)
	btn_green.grid(row = 6, column = 0, sticky = 'new', padx = 5, pady = 5,)
	btn_blue.grid(row = 7, column = 0, sticky = 'new', padx = 5, pady = 5,)
	
	# btn5.grid(row = 5, column = 0, sticky = 'new', padx = 5, pady = 5,)


	frm_modifications.grid(row = 1, column = 0,sticky = 'nsw')

def imageBox():
	frm_imageBox = tk.Frame(window, width = 600, height = 400)
	label = tk.Label(frm_imageBox, image = image,bg = '#282923')
	label.pack()
	frm_imageBox.grid(row = 1, column = 0)

def toGray():
	global isGray
	global image
	global check
	isGray = True
	faces = __faces('',0)
	if faces > 0 and check == False:
		check = not check
		imageRaw = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
	else:
		imageRaw = collect('',0)
		imageRaw = cv2.cvtColor(imageRaw, cv2.COLOR_BGR2GRAY) # pentru a nu sterge patratul
	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)

def crop():
	global isGray
	global image
	global check
	scale_percent = 100
	faces = __faces('',0)
	if faces > 0 and check == False:
		check = not check
		imageRaw = cv2.imread(path)
		b,g,r = cv2.split(imageRaw)
		imageRaw = cv2.merge((r,g,b))
	else:
		imageRaw = collect('',0)

	if isGray == False:
			h,w,c = imageRaw.shape
	else:
		h,w = imageRaw.shape

	if w >= 2100 or h >= 2100:
		scale_percent = 15
	elif w > 700 or h > 700 and w < 2000 and h < 2000:
		scale_percent = 40
	width = int(imageRaw.shape[1] * scale_percent / 100)
	height = int(imageRaw.shape[0] * scale_percent / 100)
	dsize = (width, height)
	imageRaw = cv2.resize(imageRaw, dsize)

	imageRaw = imageRaw[50:h, 50:w] # trebuie de modificat 
	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)

def red():
	global image
	scale_percent = 100
	imageRaw = cv2.imread(path)
	b,g,r = cv2.split(imageRaw)
	imageRaw = cv2.merge((r,g,b))

	h,w,c = imageRaw.shape
	if w >= 2100 or h >= 2100:
		scale_percent = 15
	elif w > 700 or h > 700 and w < 2000 and h < 2000:
		scale_percent = 40
	width = int(imageRaw.shape[1] * scale_percent / 100)
	height = int(imageRaw.shape[0] * scale_percent / 100)
	dsize = (width, height)
	imageRaw = cv2.resize(imageRaw, dsize)

	hsv = cv2.cvtColor(imageRaw, cv2.COLOR_BGR2HSV)
	lower_red = np.array([70,100,50])
	upper_red = np.array([180,255,255])
	mask = cv2.inRange(hsv, lower_red, upper_red)
	imageRaw = cv2.bitwise_and(imageRaw, imageRaw, mask=mask) 

	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)

def green():
	global image
	scale_percent = 100
	imageRaw = cv2.imread(path)
	b,g,r = cv2.split(imageRaw)
	imageRaw = cv2.merge((r,g,b))

	h,w,c = imageRaw.shape
	if w >= 2100 or h >= 2100:
		scale_percent = 15
	elif w > 700 or h > 700 and w < 2000 and h < 2000:
		scale_percent = 40
	width = int(imageRaw.shape[1] * scale_percent / 100)
	height = int(imageRaw.shape[0] * scale_percent / 100)
	dsize = (width, height)
	imageRaw = cv2.resize(imageRaw, dsize)

	hsv = cv2.cvtColor(imageRaw, cv2.COLOR_BGR2HSV)
	lower_green = np.array([50,100,50])
	upper_green = np.array([70,255,255])
	mask = cv2.inRange(hsv, lower_green, upper_green)
	imageRaw = cv2.bitwise_and(imageRaw, imageRaw, mask=mask) # gut

	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)

def blue():
	global image
	scale_percent = 100
	imageRaw = cv2.imread(path)
	b,g,r = cv2.split(imageRaw)
	imageRaw = cv2.merge((r,g,b))

	h,w,c = imageRaw.shape
	if w >= 2100 or h >= 2100:
		scale_percent = 15
	elif w > 700 or h > 700 and w < 2000 and h < 2000:
		scale_percent = 40
	width = int(imageRaw.shape[1] * scale_percent / 100)
	height = int(imageRaw.shape[0] * scale_percent / 100)
	dsize = (width, height)
	imageRaw = cv2.resize(imageRaw, dsize)

	hsv = cv2.cvtColor(imageRaw, cv2.COLOR_BGR2HSV)
	lower_red = np.array([0,100,100])
	upper_red = np.array([230,255,255])
	mask = cv2.inRange(hsv, lower_red, upper_red)
	imageRaw = cv2.bitwise_and(imageRaw, imageRaw, mask=mask) # gut

	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)

def mirror():
	global image
	global check
	faces = __faces('',0)
	if faces > 0 and check == False:
		check = not check
		imageRaw = cv2.imread(path)
		b,g,r = cv2.split(imageRaw)
		imageRaw = cv2.merge((r,g,b))
	else:
		imageRaw = collect('',0)
	
	imageRaw = cv2.flip(imageRaw, 1)

	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)

def rotate():
	global image
	global check
	faces = __faces('',0)
	if faces > 0 and check == False:
		check = not check
		imageRaw = cv2.imread(path)
		b,g,r = cv2.split(imageRaw)
		imageRaw = cv2.merge((r,g,b))
	else:
		imageRaw = collect('',0)
	
	imageRaw = cv2.rotate(imageRaw, cv2.ROTATE_90_CLOCKWISE)

	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)

def negativ():
	global image
	global check
	faces = __faces('',0)
	if faces > 0 and check == False:
		check = not check
		imageRaw = cv2.imread(path)
		b,g,r = cv2.split(imageRaw)
		imageRaw = cv2.merge((r,g,b))
	else:
		imageRaw = collect('',0)
	b,g,r = cv2.split(imageRaw)
	imageRaw = cv2.merge((r,g,b))
	image = ImageTk.PhotoImage(image = Image.fromarray(imageRaw))
	imageBox()
	collect(imageRaw,1)


def collect(arg,code):
	global imageRaw
	if code == 1:
		imageRaw = arg
	elif code == 0:
		return imageRaw

def __faces(arg,code):
	global faces
	if code == 1:
		faces = arg
	elif code == 0:
		return faces

menuBar()
modificationBar()

window.mainloop()





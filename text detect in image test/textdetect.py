from os import read
import easyocr as eo
import cv2

import removetext
import textfill

import PIL

from PIL import Image
from PIL  import ImageFont, ImageDraw





reader = eo.Reader(['ko'])

# fname = "ch32 first text original.jpg"
fname = "ch32 raw test.jpg"


#result = reader.readtext("manhwa trial cleaned.jpg")
result = reader.readtext(fname, paragraph=True)

frame = cv2.imread(fname)
img = frame

#gets the bounding box of the first paragraph of text (4 coordinates for 4 points of rectangle)
box = result[0][0]

img = removetext.get_new_img(box, img)


#text = result[0][1]
#text to be outputted, should be the translated text, but placeholder for now
# text = "I don’t know what changes have happened to you."
text = "THAT'S...!!"
# text = "ice arrow!!"

#opencv has image in bgr so have to convert to rgb
pilimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#convert opencv img to PIL img for text drawing
image = Image.fromarray(pilimg)

#image.show()

#object to draw on image
# draw = ImageDraw.Draw(image)

#x and y coordinate of top left corner of paragraph
x, y = box[0][0], box[0][1]

#set to 10 just to display font above the image
#y=10

#keep track of height and width of bounding box of paragraph
boxWidth = box[1][0] - box[0][0]
boxHeight = box[2][1] - box[1][1]
# print("b", box, "w", boxWidth, "h", boxHeight)

# color = (255, 255, 255)
color = (0,0,0)
font = "Fonts\wildwordsbold.ttf"

border = (True, (110, 0, 0, 255), 0)

# print("size", image.size)

image = textfill.write_text_to_box(tuple(box[0]), boxWidth, boxHeight, text, color, image, font, border)

image.save("proofpic.png")

 ############################################## TODO: get the same border and text color in original text so it matches
#     #text border color
#     borderColor = (110, 0, 0, 255)
#     # borderColor = (255,0,0, 255)
#     textColor = (0,0, 200, 255)
#     borderThickness = 0

# #pick font
# ############################################## TODO: pick matching font if necessary
# font = ImageFont.truetype("Fonts\wildwordsbold.ttf", int(0.75*lineHeight))



# draws the bounding box for testing purposes
np = (box[0][0], box [0][1])
ip = np
for p in box:
    p = (p[0], p[1])
    img = cv2.line(frame, np, p, (0,0,0), 3)
    np = p

img = cv2.line(frame, np, ip, (0,0,0), 3)


#prints the result returned from the easyocr lib
print ("results", result)

#shows the output
cv2.imshow("new img", img)
cv2.waitKey(0)


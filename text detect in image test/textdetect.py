from os import read
import easyocr as eo
import cv2
import removetext

import PIL

from PIL import Image
from PIL  import ImageFont, ImageDraw


import textwrap

reader = eo.Reader(['ko'])

fname = "ch32 first text original.jpg"


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
text = "ice arrow!!"

#opencv has image in bgr so have to convert to rgb
pilimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#convert opencv img to PIL img for text drawing
image = Image.fromarray(pilimg)

image.show()

#object to draw on image
draw = ImageDraw.Draw(image)

#x and y coordinate of top left corner of paragraph
x, y = box[0][0], box[0][1]

#set to 10 just to display font above the image
#y=10

####################################### TODOfigure a good split for text so it is legible
wrapped = text.split(" ")
#wrap the output text (keep at 6 characters wide)
# wrapped = textwrap.wrap(text, width=6)

print("wrapped", wrapped)
#keep track of height and width of bounding box of paragraph
boxWidth = box[1][0] - box[0][0]
boxHeight = box[2][1] - box[1][1]

#set height of each line s.t. the text fits perfectly into bounding box
lineHeight = int(boxHeight / len(wrapped))

print("lineheight", lineHeight)

#get the centre line of bounding box to help with text alignment
midline = int(boxWidth/2) + x

#draw each line of the output text, staying within boundingbox boundaries
#also draw a border around the text
for i, line in enumerate(wrapped):

    print("midline", midline)
    print ("x", x, "y", y)

    #fontImg = ImageFont.truetype("Fonts/kor-EULCHE.otf", tsTran[1])
    #pick font
    ############################################## TODO: pick matching font if necessary
    font = ImageFont.truetype("Fonts\wildwordsbold.ttf", int(0.75*lineHeight))

    #gets the width and height of the translated (output) text with the specific font
    w, h = draw.textsize(line, font=font)

    #sets the x-coordinate of the outputted text such that the text will be centred in boundingbox
    x = midline - int(w/2)

    ############################################## TODO: get the same border and text color in original text so it matches
    #text border color
    borderColor = (110, 0, 0, 255)
    # borderColor = (255,0,0, 255)
    textColor = (0,0, 200, 255)
    borderThickness = 0


    # orthogonal border
    draw.text((x-borderThickness, y), line, font=font, fill=borderColor)
    draw.text((x+borderThickness, y), line, font=font, fill=borderColor)
    draw.text((x, y-borderThickness), line, font=font, fill=borderColor)
    draw.text((x, y+borderThickness), line, font=font, fill=borderColor)

    # diagonal border
    draw.text((x-borderThickness, y-borderThickness), line, font=font, fill=borderColor)
    draw.text((x+borderThickness, y-borderThickness), line, font=font, fill=borderColor)
    draw.text((x-borderThickness, y+borderThickness), line, font=font, fill=borderColor)
    draw.text((x+borderThickness, y+borderThickness), line, font=font, fill=borderColor)

    #drawing the actual line of text
    draw.text((x, y), line, font=font, fill=textColor)

    
    #increment y to the new line for next line
    y = y + lineHeight
                

#store new image
image.save("manhwawithtxt2.jpg")
#img = cv2.rectangle(frame, (box[0][0], box[0][1]), (box[2][0], box [2][1]), (0,0,0,), 3)
#cv2.imshow("Result Image", img)
#cv2.waitKey(0)



#draws the bounding box for testing purposes
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


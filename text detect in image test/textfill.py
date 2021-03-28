from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# class ImageText(object):
#     def __init__(self, filename_or_size, mode='RGBA', background=(0, 0, 0, 0),
#                  encoding='utf8'):
#         if isinstance(filename_or_size, str):
#             self.filename = filename_or_size
#             self.image = Image.open(self.filename)
#             self.size = self.image.size
#         elif isinstance(filename_or_size, (list, tuple)):
#             self.size = filename_or_size
#             self.image = Image.new(mode, self.size, color=background)
#             self.filename = None
#         self.draw = ImageDraw.Draw(self.image)
#         self.encoding = encoding

def save(self, image, filename=None):
    image.save(filename or self.filename)

def get_font_size(self, text, font, max_width=None, max_height=None):
    if max_width is None and max_height is None:
        raise ValueError('You need to pass max_width or max_height')
    font_size = 1
    text_size = self.get_text_size(font, font_size, text)
    if (max_width is not None and text_size[0] > max_width) or \
        (max_height is not None and text_size[1] > max_height):
        raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                text_size)
    while True:
        if (max_width is not None and text_size[0] >= max_width) or \
            (max_height is not None and text_size[1] >= max_height):
            return font_size - 1
        font_size += 1
        text_size = self.get_text_size(font, font_size, text)

def write_text(dim, text, image, font_filename, font_size=11,
                color=(0, 0, 0), max_width=None, max_height=None):
    x,y = dim
    draw = ImageDraw.Draw(image)
    if font_size == 'fill' and \
        (max_width is not None or max_height is not None):
        font_size = get_font_size(text, font_filename, max_width,
                                        max_height)
    text_size = get_text_size(font_filename, font_size, text)
    font = ImageFont.truetype(font_filename, font_size)
    if x == 'center':
        x = (image.size[0] - text_size[0]) / 2
    if y == 'center':
        y = (image.size[1] - text_size[1]) / 2
    draw.text((x, y), text, font=font, fill=color)
    return text_size

def get_text_size(font_filename, font_size, text):
    font = ImageFont.truetype(font_filename, font_size)
    return font.getsize(text)

def write_text_box(image, dim, text, box_width, font_filename, box_height, 
                    font_size=11, color=(0, 0, 0), place='left',
                    justify_last_line=False, write=False, borderThickness=0):
    x, y = dim
    lines = []
    line = []
    words = text.split()
    for word in words:
        new_line = ' '.join(line + [word])
        size = get_text_size(font_filename, font_size, new_line)
        text_height = (size[1] + borderThickness/2) * 1.5
        last_line_bleed = text_height - size[1]
        if size[0] <= box_width:
            line.append(word)
        else:
            lines.append(line)
            line = [word]
    if line:        
        lines.append(line)
    lines = [' '.join(line) for line in lines if line]

    height = (box_height - len(lines)*text_height + last_line_bleed)/2 + y

    # height = y
    for index, line in enumerate(lines):
        
        # if place == 'left':
        #     if write:
        #         write_text((x, height), line, image, font_filename, font_size,
        #                     color)
        # elif place == 'right':
        #     total_size = get_text_size(font_filename, font_size, line)
        #     x_left = x + box_width - total_size[0]
        #     if write:
        #         write_text((x_left, height), line, image, font_filename,
        #                     font_size, color)
        if place == 'center':
            total_size = get_text_size(font_filename, font_size, line)
            x_left = int(x + ((box_width - total_size[0]) / 2))
            
            if write:
                write_text((x_left, height), line, image, font_filename,
                            font_size, color)
        height += text_height
        # elif place == 'justify':
        #     words = line.split()
        #     if (index == len(lines) - 1 and not justify_last_line) or \
        #         len(words) == 1:
        #         if write:
        #             write_text((x, height), line, image, font_filename, font_size,
        #                         color)
        #         continue
        #     line_without_spaces = ''.join(words)
        #     total_size = get_text_size(font_filename, font_size,
        #                                     line_without_spaces)
        #     space_width = (box_width - total_size[0]) / (len(words) - 1.0)
        #     start_x = x
        #     for word in words[:-1]:
        #         if write:
        #             write_text((start_x, height), word, image, font_filename,
        #                         font_size, color)
        #         word_size = get_text_size(font_filename, font_size,
        #                                         word)
        #         start_x += word_size[0] + space_width
        #     last_word_size = get_text_size(font_filename, font_size,
        #                                         words[-1])
        #     last_word_x = x + box_width - last_word_size[0]
        #     if write:
        #         write_text((last_word_x, height), words[-1], image, font_filename,
        #                     font_size, color)
    return (box_width, int(height - y))



def write_text_to_box(box_start, boxWidth, boxHeight, text, color, img, font, border):


    borderbool, bordercolor, borderthickness = border
    
    fs = 1
    boxdim = write_text_box(img, box_start, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=color, place='center')

    while (boxdim[1] <= boxHeight):# and boxdim[0] <= boxWidth):
        # print(boxdim)
        fs += 1
        boxdim = write_text_box(img, box_start, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=color, place='center')
    fs -=1
    

    if borderbool:

        #orthogonal border
        box_startn = (box_start[0]-borderthickness, box_start[1])
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)
        
        box_startn = (box_start[0], box_start[1]-borderthickness)
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)

        box_startn = (box_start[0]+borderthickness, box_start[1])
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)

        box_startn = (box_start[0], box_start[1]+borderthickness)
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)


        #diagonal border
        box_startn = (box_start[0]-borderthickness, box_start[1]-borderthickness)
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)
        
        box_startn = (box_start[0]-borderthickness, box_start[1]+borderthickness)
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)

        box_startn = (box_start[0]+borderthickness, box_start[1]-borderthickness)
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)

        box_startn = (box_start[0]+borderthickness, box_start[1]+borderthickness)
        write_text_box(img, box_startn, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=bordercolor, place='center', write=True, borderThickness=borderthickness)

    # draw = ImageDraw.Draw(img)
    # draw.line((box_start, (box_start[0], box_start[1]+boxHeight)), fill=0)
    # draw.line(((box_start[0], box_start[1]+boxHeight), (box_start[0]+boxWidth, box_start[1]+boxHeight) ), fill=0)
    # print(box_start, boxdim)
    
    write_text_box(img, box_start, text, box_width=boxWidth, font_filename=font,
                    box_height=boxHeight, font_size=fs, color=color, place='center', write=True, borderThickness=borderthickness)

    return img


# # text = 'Python is a cool programming language. You should learn it!'
# text = 'ice arrow'
# # box = [[26, 257], [368, 257], [368, 450], [26, 450]]
# box = [[461, 631], [605, 631], [605, 751], [461, 751]]

# boxWidth = box[1][0] - box[0][0]
# boxHeight = box[2][1] - box[1][1]

# color = (255, 255, 255)
# font = "Fonts\wildwordsbold.ttf"

# border = (True, (110, 0, 0, 255), 2)
# # img = ImageText((800, 600), background=(255, 255, 255, 200)) # 200 = alpha
# image = None
# import cv2

# img = cv2.imread("manhwawithtxt2 removed txt.jpg")
# img = Image.fromarray(img)
# image = write_text_to_box(tuple(box[0]), boxWidth, boxHeight, text, color, img, font, border)

# image.save("sample image w border n th.png")
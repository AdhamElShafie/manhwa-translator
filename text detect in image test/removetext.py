import cv2

def get_new_img(box, img):
    # box = [[26, 257], [368, 257], [368, 450], [26, 450]]

    box_y0, box_y1, box_x0, box_x1 = box[0][1], box[2][1], box[0][0], box[2][0]

    # img = cv2.imread("manhwa trial cleaned.jpg")

    #print(img[box_tl:box_bl, box_tr:box_br])
    sizediff = 15
    imgbox = img[box_y0-sizediff:box_y1+sizediff, box_x0-sizediff:box_x1+sizediff]
    show("boximg", imgbox)
    gray = cv2.cvtColor(imgbox, cv2.COLOR_BGR2GRAY)
    show("gray", gray)


    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    show("thresh", thresh)
    #mask = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)[1][:,:,0]
    #print(len(mask))
    #cv2.imshow("mask", mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    inverted_thresh = 255-thresh

    dilate = cv2.dilate(inverted_thresh, kernel, iterations=5)
    show("dilate", dilate)

    # cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dst = cv2.inpaint(imgbox, dilate, 7, cv2.INPAINT_NS)
    show("dst", dst)

    img[box_y0-sizediff:box_y1+sizediff, box_x0-sizediff:box_x1+sizediff] = dst

    show("final", img)
    #cv2.waitKey(0)
    
    return img


def show(name, inp):
    return
    #cv2.imshow(name, inp)

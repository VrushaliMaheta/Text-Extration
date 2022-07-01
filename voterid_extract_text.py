import easyocr as eo
import re
import numpy as np
import imutils
import easyocr
import cv2
from PIL import Image, ImageEnhance

"""rotated = "Images/papa_voterid_front.jpeg"
img = cv2.imread(rotated)
img2=Image.fromarray(img)
enhancer = ImageEnhance.Brightness(img2)

factor = 1.5 #gives original image
im_output = enhancer.enhance(factor)
eimage=np.asarray(im_output)
r,g,b=cv2.split(eimage)
eimage=cv2.merge([b,g,r])

reader = eo.Reader(['en'])
result = reader.readtext(eimage)
# list to String (easy ocr return list)
text = ""
for res in result:
   text += res[1] + ' '

def voter_card_front(text):
    Name = ""
    voter_rep ={}

    if(re.search(r"\bName\w*(?:\s+[A-z ]\w*(?:\s+[A-z ]\w*))",text)):
        x = re.search(r"\bName\w*(?:\s+[A-z ]\w*(?:\s+[A-z ]\w*))",text)
        xx = x.group()
        xxx = xx.replace("Name ","")
        voter_rep["Name"] = xxx

    if(re.search(r"\bFather\'s Name\w*(?:\s+[A-z ]\w*)", text)):
        y = re.search(r"\bFather\'s Name\w*(?:\s+[A-z ]\w*)", text)
        yy = y.group()
        yyy = yy.replace("Father\'s Name ","")
        voter_rep["Father Name"] = yyy
    elif(re.search(r"\bHusband\'s Name\w*(?:\s+[A-z ]\w*)", text)):
        z = re.search(r"\bHusband\'s Name\w*(?:\s+[A-z ]\w*)", text)
        zz = z.group()
        zzz = zz.replace("Husband\'s Name ", "")
        voter_rep["Husband Name"] = zzz
    else:
        a = "Not Fatch Father Name/Husband Name"
        voter_rep["Father Name"] = a

    return  voter_rep
    
print(voter_card_front(text))
"""

rotated = "Images/mummy_voterid_back.jpeg"
img = cv2.imread(rotated)
img2=Image.fromarray(img)
enhancer = ImageEnhance.Brightness(img2)

factor = 1.5 #gives original image
im_output = enhancer.enhance(factor)
eimage=np.asarray(im_output)
r,g,b=cv2.split(eimage)
eimage=cv2.merge([b,g,r])

reader = eo.Reader(['en'])
result = reader.readtext(eimage)
# list to String (easy ocr return list)
text = ""
for res in result:
   text += res[1] + ' '

print(text)

def voter_card_back(text):
    gender = ""
    dob = ""
    address = ""
    voter_rep = {}

    # exract gender from image
    if (re.search("female", text, re.IGNORECASE)):
        gender = "Female"
    elif (re.search("male", text, re.IGNORECASE)):
        gender = "Male"
    else:
        gender=""
    #print("Gender: ",gender)
    voter_rep["Gender"] = gender

    #extract date of birth or age from image
    if(str(re.search(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", text).group()).replace("]", "").replace("[", "").replace("'", "")):
        dob = str(re.search(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", text).group()).replace("]", "").replace("[", "").replace("'", "")
    elif(str(re.search(r"[\d]{1,2}", text).group()).replace("]", "").replace("[", "").replace("'", "")):
        dob = str(re.search(r"[\d]{1,2}", text).group()).replace("]", "").replace("[", "'", "")
    else:
        dob = "Not fetch Date of Birth/Age"

    voter_rep["Date of Birth/Age"] = dob

    #extract address from image
    if(re.search(r"\bAddress(.+?)Dist.(?:\s+[A-Z]\w*)",text)):
        x = re.search(r"\bAddress(.+?)Dist.(?:\s+[A-Z]\w*)",text).group()
        add = x.replace("Address ","")
    else:
        add = "Address not fetch"

    voter_rep["Address"] = add

    return voter_rep

print(voter_card_back(text))

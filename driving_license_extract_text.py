from PIL import Image,ImageEnhance
import pytesseract
import datetime
import easyocr as eo
import sys
import os
import os.path
import easyocr
import re
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

rotated = "Images/mummy_driving_license.jpg"
img = cv2.imread(rotated)
img2=Image.fromarray(img)
enhancer = ImageEnhance.Brightness(img2)

factor = 1.5 #gives original image
im_output = enhancer.enhance(factor)
eimage=np.asarray(im_output)
r,g,b=cv2.split(eimage)
eimage=cv2.merge([b,g,r])

"""kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
image_sharp = cv2.filter2D(src=eimage, ddepth=-1, kernel=kernel)"""

reader = eo.Reader(['en'])
result = reader.readtext(eimage)
# list to String (easy ocr return list)
text = ""
for res in result:
   text += res[1] + ' '

def driving_license(text):
   dri_rep = {}
   if (re.search(r"([\d]{1,4}-[\d]{1,4}-[\d]{1,4})", text)):
      x = re.findall(r"([\d]{1,4}-[\d]{1,4}-[\d]{1,4})", text)
      first_issue = x[0]
      expire_date = x[1]
      birth_date = x[2]
   elif (re.search(r"([\d]{1,4}/[\d]{1,4}/[\d]{1,4})", text)):
      x = re.findall(r"([\d]{1,4}/[\d]{1,4}/[\d]{1,4})", text)
      y = re.findall(r"([\d]{1,4}\|[\d]{1,4}/[\d]{1,4})", text)
      first_issue = x[0]
      expire_date = x[3]
      birth_date = y[0]
   else:
      first_issue = "Date of issue not fetch"
      expire_date = "Expire date not fetch"
      birth_date = "Birth date not fetch"

   dri_rep["Date of First Issue"] = first_issue
   dri_rep["Expire Date"] = expire_date
   dri_rep["Birth Date"] = birth_date

   s = text.split(" ")
   strings_with_states = []
   count = 0

   list_of_states = {'JK', 'HP', 'PN', 'CH', 'UK', 'UA', 'HR', 'DL', 'RJ', 'UP', 'BR', 'SK', 'AR', 'AS', 'NL', 'MN',
                     'ML', 'TR', 'MZ', 'WB', 'JH', 'OR', 'OD', 'CG', 'MP', 'GJ', 'MH', 'DD', 'DN', 'TS', 'AP', 'KA',
                     'KL', 'TN', 'PY', 'GA', 'AN', 'LD'}

   for word in s:
      for state in list_of_states:
         if state in word:
            strings_with_states.append(word)

   for string in strings_with_states:
      for i in string:
         if (i.isdigit()):
            count = count + 1

      if count < 13:
         index = s.index(string)
         s1 = s[index] + s[index + 1]
         if len(s) >= 15:
            for i in s1:
               if (i.isdigit()):
                  count = count + 1
            if count > 13:
               s1 = s1[-16:]
               dri_rep["Driving License Number"] = s1
               break
               break
      else:
         dri_rep["Driving License Number"] = string
         break
         break

   name=''
   if 'Name' in s:
      index = s.index('Name')
      name =  s[index + 1] + ' ' + s[index + 2]
   elif 'NAME' in s:
      index = s.index('NAME')
      name = s[index+1]+' ' +s[index+2]
   elif 'MAME' in s:
      index = s.index('MAME')
      name = s[index+1]+' '+s[index+2]
   else:
      name = "Name of the card holder not fetch"
   dri_rep["Name of license holder"] = name
   return dri_rep

print(driving_license(text))

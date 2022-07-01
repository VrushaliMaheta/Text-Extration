import easyocr as eo
import re
import numpy as np
import imutils
import easyocr

rotated = "Images/papa_aadhar.jpg"
reader = eo.Reader(['en'])
result = reader.readtext(rotated)
# list to String (easy ocr return list)
text = ""
for res in result:
   text += res[1] + ' '

    
def camel_case_split(str):
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)

def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s

def aadhar_card(text):
    Name = ""
    gender= ""
    dob = ""
    a_number =""
    aadhar_rep ={}
    rx = r"\b[A-Z]\w*(?:\s+[A-Z]\w*)+"
    result = [" ".join(x.split()) for x in re.findall(rx, text)]
    nameArr = []
    for j in result:
        arrInner = camel_case_split(j)
        for k in arrInner:
            if len(k) >= 4:
                if is_camel_case(k):
                    if k != 'Government' and k != 'India' and k != 'Male' and k != 'Mobile' and k != 'Female' and k != 'Father' and k != 'Year' and k != 'Birth':
                        nameArr.append(k)
                    # print(k)
    #print("Name: ",str(nameArr).replace("]", "").replace("[","").replace("'", "").replace(",", ""))
    name = str(nameArr).replace("]", "").replace("[","").replace("'", "").replace(",", "")
    aadhar_rep["Name"] = name

    if (re.search("female", text, re.IGNORECASE)):
        gender = "Female"
    elif (re.search("male", text, re.IGNORECASE)):
        gender = "Male"
    else:
        gender=""
    #print("Gender: ",gender)
    aadhar_rep["Gender"] = gender

    if (re.search("Year of Birth", text, re.IGNORECASE) or (re.search("Year", text, re.IGNORECASE) and re.search("Birth", text, re.IGNORECASE))):
        res = re.search(r'\d{4}', text)
        if res:
            #print("year of birth: ",res.group())
            dob = res.group()
        else:
            print("Year of birth not fetch")
            dob = "Not Fetch"
    else:
        dob = str(re.findall(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", text)).replace("]", "").replace("[","").replace("'", "")

    aadhar_rep["Date/Year of Birth"] = dob

    testStr = text.replace(" ", "")
    number = re.search(r'\d{12}', testStr)
    if number:
        #print("Aadhar number: ",number.group())
        a_number=number.group()
    else:
        print("Aadhar number not fetch")
        a_number = "Not Fetch"
    aadhar_rep["Aadhar Number"] = a_number
    return  aadhar_rep

print(aadhar_card(text))

print("Program Started: Metricify.")

print("[Step 1 of 6] Loading ... ", end="")

import sys

#sys.path.append("/usr/local/lib/python3.9/dist-packages")

import pytesseract
from pytesseract import pytesseract
import PIL
from PIL import Image, ImageDraw, ImageFont
import cv2
import csv
import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import os
from pdf2jpg import pdf2jpg
import fpdf

#from fpdf import output

filename = "phb.pdf" #askopenfilename() # show an "Open" dialog box and return the path to the selected file
name = filename.split(".")[0] + "-metric.pdf"

value_conversions = {
"feet": 0.3048,
"foot": 0.3048,
"ft": 0.3048,
"inches": 2.54,
"inch": 2.54,
#"ins": 2.54,
"miles": 1.60934,
"mile": 1.60934,
#"mi": 1.60934,
"lb": 0.45359,
"Ib": 0.45359,
"lbs": 0.45359,
"pounds": 0.45359,
"oz": 28.3495,
"ounces": 28.3495,
"ounce": 28.3495,
"gallons": 3.78541,
"gal": 3.78541
}

unit_conversions = {
"feet": "metres",
"foot": "metre",
"ft": "m",
"inches": "cm",
"inch": "cm",
"ins": "cm",
"miles": "km",
"mile": "km",
"mi": "km",
"lb": "kg",
"Ib": "kg",
"lbs": "kg",
"pounds": "kilograms",
"oz": "g",
"ounces": "grams",
"ounce": "gram",
"gallons": "litres",
"gal": "litres"
}

dir_ = "/".join(__file__.split("/")[:-1])

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

file = open(filename, "rb")

fileReader = PyPDF2.PdfFileReader(file)

n = fileReader.numPages

font = ImageFont.truetype('BOD_CB.TTF', 33)

#blank = Image.open("blank.jpg")

made = False
pdf = None

edits = 0


print("Done.")

print("[Step 2 of 6] Commencing metrification ...")

def append_pdf(inp, output):
    [output.addPage(inp.getPage(page_num)) for page_num in range(inp.numPages)]


for i in range(0, n):

    print("Processing page " + str(i) + ", ", end="")

    result = pdf2jpg.convert_pdf2jpg(filename, dir_, pages=str(i))

    #print(result)

    #print("Flag")

    loc = dir_ + "/" + filename + "_dir/" + str(i) + "_" + filename + ".jpg"

    #print("Flag")

    img = Image.open(loc)

    #print("Flag")

    width, height = img.size

    pdf = fpdf.FPDF("P", "pt", (width, height))

    #print("Flag")

    #blank = blank.resize((width, height))

    #print(img.size, blank.size)

    draw = ImageDraw.Draw(img)

    data = pytesseract.image_to_boxes(img, lang='eng')

    forks = data.split("\n")

    string = ""

    print(str((i / n)*100)[:5] + "% complete, " + str(edits) + " edits made.")

    found = False

    

    for d in range(0, len(forks)):

        #print(d*100 / len(forks))
        
        aspects = forks[d].split(" ")

        if not len(aspects):
            continue
        
        string += aspects[0]

        for k in value_conversions.keys():
            
            if string.lower().endswith(k):
                
                sect = string[-(len(k)+8):]

                
                for char in range(0, len(sect)):
                    if sect[char].isdigit():
                        sect = sect[char:]
                        break
                else:
                    continue


                redo = False
                for bad in "()[],.;:|": # Steer clear of anything with weird punctuation.
                    if bad in sect:
                        redo = True
                        break
                if redo:
                    continue
                

                # Avoid editing out any mathematical operators.
                if "+" in sect:
                    sect = sect.split("+")[1]
                if "=" in sect:
                    sect = sect.split("=")[1]

                # Damage or currency valeues never have imperial units. Don't edit these.
                if "damage" in sect or "of" in sect or "leve" in sect or "mind" in sect:
                    continue
                if "gp" in sect or "sp" in sect or "cp" in sect:
                    print("[Money]", sect)
                    continue


                #print(sect)

                if len(aspects) < 4:
                    print("Bad Aspect", aspects)
                    continue
                
                x2 = int(aspects[3])
                y2 = height - int(aspects[4]) - 10

                startAspect = forks[d - len(sect) + 1].split(" ")

                x1 = int(startAspect[1])
                y1 = height - int(startAspect[2]) + 5


                print("Gettinc colour")


                colour = img.load()[x1, y1]

                draw.rectangle([(x1, y1), (x2, y2)], outline=colour, fill=colour)

                print("Drawn.")

                #cap = blank.copy()
                #cap = cap.crop((x1, y2, x2, y1))
                #img.paste(cap, (x1, y2))

                sect = sect.replace("-", "")



                # Tidy edits with conjunctions in the middle.
                
                to = False
                a = None
                valA = None

                if "to" in sect:
                    to = "to"
                    a, sect = sect.split("to")
                elif "and" in sect:
                    to = "and"
                    a, sect = sect.split("and")
                elif "by" in sect:
                    to = "by"
                    a, sect = sect.split("by")

                for char in range(0, len(sect)):
                    if sect[char].isdigit():
                        sect = sect[char:]
                        break
                else:
                    continue

                digFound = -1

                sect = "0" + sect

                for char in range(0, len(sect)):
                    if sect[char].isdigit() and digFound == -1:
                        digFound = char
                    elif digFound > -1 and char != "0" and not sect[char].isdigit():
                        imp = sect[digFound:char]
                        break
                else:
                    print("[Warning]", sect)
                    continue


                #print("Imp:", imp)

                if to != False:
                    for char in range(0, len(a)):
                        if not a[char].isdigit():
                            a = a[:char]
                            break

                unit = k

                try:
                    value = round(value_conversions[unit]*float(imp), 0)
                    value = int(str(value).split(".")[0])

                    if to != False:
                        valA = round(value_conversions[unit]*float(a), 0)
                        valA = int(str(valA).split(".")[0])

                except ValueError:
                    print("[ValErr]")
                unit = unit_conversions[unit]

                if to != False:
                    text = str(valA) + " " + to + " " + str(value) + " " + unit
                else:
                    text = str(value) + " " + unit

                #print(text)

                draw.text((x1 - 2, y2 - 1), str(text), font=font, fill=(45, 32, 32))

                found = True

    if found:
        img.save("temp.jpg")

        pdf.add_page()
        pdf.image("temp.jpg", 0, 0)

        edits += 1

        broken = True

    else:
        #print("No imp.")
        pdf.add_page()
        pdf.image(loc, 0, 0)

    
    if not made:
        pdf.output(dir_ + "/" + str(i+1) + name, "F")
        made = True
        
    else:
        pdf.output("temp.pdf", "F")
        
        merger = PdfFileMerger()
        
        merger.append(dir_ + "/" + str(i) + name)

        merger.append(dir_ + "/temp.pdf")

        #merger.write(name)

        merger.write(dir_ + "/" + str(i+1) + name)
        os.remove(dir_ + "/" + str(i) + name)

        merger.close()
        

print("Cleaning up...")

try:
    os.remove("temp.jpg")
except:
    pass

try:
    os.remove(loc)
except:
    pass

#ocrmypdf input.pdf output.pdf
      
print("Done.")

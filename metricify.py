print("Program Started: Metricify.")

print("Loading ... ", end="")

# Import modules
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


platform = None

if "/" in __file__: # Determine the platform the program is running on.
    platform = "linux"
else:
    platform = "windows"



if platform == "linux":
    dir_ = "/".join(__file__.split("/")[:-1])
elif platform == "windows":
    dir_ = "\\".join(__file__.split("\\")[:-1])

    

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing


file = open(filename, "rb") # Open the input file.

fileReader = PyPDF2.PdfFileReader(file) # Open the file in the pdf reader.

n = fileReader.numPages # Get number of pages in the input file.

font = ImageFont.truetype('BOD_CB.TTF', 33) # Load the edit font.


made = False
pdf = None
edits = 0 # Counts edits we have made.


print("Done.") # Done loading.

print("Commencing metrification ...")


def append_pdf(inp, output): # Adds a page to a pdf.
    [output.addPage(inp.getPage(page_num)) for page_num in range(inp.numPages)]


for i in range(0, n): # Iterate through all pages.

    print("Processing page " + str(i) + ", ", end="")

    result = pdf2jpg.convert_pdf2jpg(filename, dir_, pages=str(i)) # Convert the current page to a .jpg image.

    loc = ""

    if platform == "linux":
        loc = dir_ + "/" + filename + "_dir/" + str(i) + "_" + filename + ".jpg"
    elif platform == "windows":
        loc = dir_ + "\\" + filename + "_dir\\" + str(i) + "_" + filename + ".jpg"


    img = Image.open(loc) # Load the image we have created of the current page.
    width, height = img.size # Get the size of this image (allows for variable sized pages).

    pdf = fpdf.FPDF("P", "pt", (width, height)) # Create a blank pdf page of the same size as the cunnent page.

    draw = ImageDraw.Draw(img) # Load the .jpg image of the current page for editing.

    data = pytesseract.image_to_boxes(img, lang='eng') # Conduct OCR to detect text on the cunnernt page.

    forks = data.split("\n") # Split this text into lines to make it easier to work with.
    # Note, this causes edits to fail if the imperial units are writen over multiple lines.

    string = "" # Stores the text of the current line in program memory.
    found = False # Hove we found anything that needs editing?

    print(str((i / n)*100)[:5] + "% complete, " + str(edits) + " edits made.")


    for d in range(0, len(forks)): # Iterates through lines of text on the page.
        
        aspects = forks[d].split(" ") # Split text into words to make it easier to work with.

        if not len(aspects): # There is no text here, let's move on.
            continue
        
        string += aspects[0] # Add first word to the line string.

        for k in value_conversions.keys(): # Iterate through possib/le imperial units.
            
            if string.lower().endswith(k): # We've found an imperial unit!
                
                sect = string[-(len(k)+8):] # Extracts a section of the line string where the imperial unit is fount.
                
                for char in range(0, len(sect)): # Iterate through letters in the general vicinity of the imperial unit.
                    if sect[char].isdigit(): # Get the part after the numbers. That will be the unit of the numbers.
                        sect = sect[char:]
                        break
                else:
                    continue # There were no numbers, it's a red herring! eg. "The hobbit had hairy feet".

                redo = False
                for bad in "()[],.;:|": # Steer clear of anything with weird punctuation for now.
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
                    #print("[Money]", sect)
                    continue

                #print(sect)

                if len(aspects) < 4: # This is a really stort line of text. Probably not an imperial value.
                    #print("Bad Aspect", aspects)
                    continue

                # Get coordinates of bottom right of the imperial value.
                x2 = int(aspects[3])
                y2 = height - int(aspects[4]) - 10

                startAspect = forks[d - len(sect) + 1].split(" ") # Get the first word of the imperial value.

                # Get coordinates of top left of the imperial value.
                x1 = int(startAspect[1])
                y1 = height - int(startAspect[2]) + 5

                colour = img.load()[x1, y1] # Take a sample of the page colour behing the imperial text.
                draw.rectangle([(x1, y1), (x2, y2)], outline=colour, fill=colour) # Patch the imperial text with background colour.


                sect = sect.replace("-", "") # Fixes weird hyphens. eg. 23-foot pole.


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


                for char in range(0, len(sect)): # Go through the text extract again and make 100% sure that we only have the units, not the number in fromt of them.
                    if sect[char].isdigit():
                        sect = sect[char:]
                        break
                else:
                    continue # In case we have "a hobbit standing in a yard with hairy feet."


                digFound = -1 # Stores the difit that we will find in front of the unit.

                sect = "0" + sect # Add a leading zero as a padder, in case the metric value has more digits that the imperial one. Especially relevant when converting inches to cm.

                for char in range(0, len(sect)): # Iterate throung the imperial text.
                    if sect[char].isdigit() and digFound == -1: # Find the first digit.
                        digFound = char # This should pick up our leading zero.
                    elif digFound > -1 and char != "0" and not sect[char].isdigit(): # Find subsequent digits.
                        imp = sect[digFound:char] # Assemble the imperial value (the numbers bit).
                        break
                else: # Something went badly wrong.
                    #print("[Warning]", sect) 
                    continue # Let's hope nobody notices.


                #print("Imp:", imp)

                if to != False: # eg. "5 to 25 feet."
                    for char in range(0, len(a)): # Get the first value.
                        if not a[char].isdigit():
                            a = a[:char]
                            break

                unit = k # This (k) should probably just be called 'unit' all along, but it works like this and I'm afraid to change it.

                try: # Convert the imperial value to metric.
                    value = value_conversions[unit]*float(imp) # Get the raw conversion.
                    
                    if value > 1: # Remove excessive decimal places.
                        value = round(value, 0)
                        value = int(str(value).split(".")[0])
                    else:
                        value = round(value, 1)
                        value = int(str(value))

                    if to != False: # In this case, we have 2 walues to convert, so do the same again.
                        valA = value_conversions[unit]*float(a)
                        
                        if valA > 1:
                            valA = round(valA, 0)
                            valA = int(str(valA).split(".")[0])
                        else:
                            valA = round(valA, 1)
                            valA = int(str(valA))

                except ValueError: # After all that, the imperial value was still invalid :(
                    continue
                    #pass
                    #print("[ValErr]")


                unit = unit_conversions[unit] # Get the metric equivalunt of our imperial unit string.
                
                if to != False: # Combine the metric value with the metric unit.
                    text = str(valA) + " " + to + " " + str(value) + " " + unit
                else:
                    text = str(value) + " " + unit

                #print(text)

                # Inser the metric text over our patch.
                draw.text((x1 - 2, y2 - 1), str(text), font=font, fill=(45, 32, 32))

                found = True # Confirm an edit has been made.


    if found: # If an edit has been made
        img.save("temp.jpg") # Save the .jpg image that we edited.

        pdf.add_page() # Add a page to our new pdf.
        pdf.image("temp.jpg", 0, 0) # Insert the edited .jpg image into the new page of the pdf.

        edits += 1 # Increment the edits counter.

    else: # There were no imperial values on the page.
        pdf.add_page() # Make a new page on the new pdf.
        pdf.image(loc, 0, 0) # Copy the old page directly to the nem page.


    if not made: # First page, create the new pdf file.
        if platform == "linux":
            pdf.output(dir_ + "/" + str(i+1) + name, "F")
        elif platform == "windows":
            pdf.output(dir_ + "\\" + str(i+1) + name, "F")
        made = True # Confirm new pdf file has been made.
        
    else: # Not the first page, add to the existing pdf file.
        pdf.output("temp.pdf", "F") # Create temporary pdf file of our new page.
        
        merger = PdfFileMerger() # Initialilse the pdf merger that will join our 2 pdf files.

        # Join the latest page onto the main pdf file.

        if platform == "linux":
            merger.append(dir_ + "/" + str(i) + name)
            merger.append(dir_ + "/temp.pdf")
            merger.write(dir_ + "/" + str(i+1) + name)
            os.remove(dir_ + "/" + str(i) + name)
        elif platform == "windows":
            merger.append(dir_ + "\\" + str(i) + name)
            merger.append(dir_ + "\\temp.pdf")
            merger.write(dir_ + "\\" + str(i+1) + name)
            os.remove(dir_ + "\\" + str(i) + name)

        merger.close() # Close the pdf merger subroutine.
        

# Clean up routines.

try:
    os.remove("temp.jpg")
except:
    pass

try:
    os.remove("temp.pdf")
except:
    pass

try:
    os.remove(loc)
except:
    pass
      
print("Done.")

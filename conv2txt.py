import os
from os import path
import sys
import cv2
from PIL import Image
from pdf2image import convert_from_path
from pdf2image import pdf2image
import tempfile
import pytesseract
import shutil
import textract
import docx
import subprocess
import re
import math


text = ''

#write logs to file
def logging(textLog):
    f = open('data/log/convErrlog.txt','a')
    f.write(textLog+'\n')
    f.close()

# get file name, extension and full name
def getFileInfo(path):
    base = os.path.basename(path)
    fileDirName, file1_ext = os.path.splitext(path)
    filename, file_ext = os.path.splitext(base)
    return base, filename, file_ext, fileDirName

#rotate image to normal pos
def rotate(imagePath, center = None, scale = 1.0):
    image = cv2.imread(imagePath, cv2.IMREAD_COLOR)

    orgAngle = int(re.search('(?<=Rotate: )\d+', pytesseract.image_to_osd(image)).group(0))

    if orgAngle != 0:
        angle=360-orgAngle
        (h, w) = image.shape[:2]

        if center is None:
            center = (w / 2, h / 2)

        # Perform the rotation
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))

        img = Image.fromarray(rotated, 'RGB')
        img.save(imagePath)

        return True

    return False

# convert file from doc or docx to text
def convertDoc2Txt(destFolder, path, info):
    text = ""
    if (info[2].lower() == '.doc'):
        try:
            subprocess.call(['soffice', '--headless', '--convert-to', 'docx', path, '--outdir', 'data/uploads'])
            doc = docx.Document('data/uploads/'+info[1]+'.docx')
            text = ""
            for para in doc.paragraphs:
                text += para.text

            f = open(destFolder+info[1]+'.txt','w')
            f.write(text)
            f.close()
        except Exception as ex:
            logging('Try to convert and read DOC file ' + path + '. Except error: ' + str(ex))

    else:
        try:
            doc = docx.Document(path)
            text = ""
            for para in doc.paragraphs:
                text += para.text

            f = open(destFolder+info[1]+'.txt','w')
            f.write(text)
            f.close()
        except Exception as ex:
            logging('Try to get text from DOCX file ' + '. Except error: ' + str(ex))

    return text

# convert file from tif to jpg
def convertImageFile2JPG(path):
    fileInfo = getFileInfo(path)

    if (fileInfo[2].lower() == '.tif') or (fileInfo[2].lower() == '.tiff'):
        try:
            im = Image.open(path)
            im.save(fileInfo[3]+'.jpg')
        except Exception as ex:
            logging('Try to open and save file ' + fileInfo[3]+'.jpg' + '. Except error: ' + str(ex))
        fileInfo = getFileInfo(fileInfo[3]+'.jpg')

    return (0, fileInfo[3]+'/', fileInfo[1], '.jpg')

# convert file from pdf to jpg
def convertPDF2JPG(path):

    numBatchPages = 20

#   maxPages = pdf2image._page_count(path)
    maxPages = len(convert_from_path(path))

    fileInfo = getFileInfo(path)
    i = 0
    try:
        os.mkdir(fileInfo[3])
    except:
        logging("Folder exists!")

    for itPage in range(1,maxPages,numBatchPages):
        pages = convert_from_path(path, dpi=600, grayscale=True, first_page=itPage, last_page=min(itPage+numBatchPages-1, maxPages))
        for page in pages:
            page.save(fileInfo[3]+'/'+fileInfo[1]+str(i)+'.jpg', 'JPEG', dpi=(600,600), quality=95)
            i += 1
    
    return (i, fileInfo[3]+'/', fileInfo[1], '.jpg')

#recognize image file and make text file
def convertImageToText(destFolder, fileInfo):
    pathToFile = fileInfo[1].replace(fileInfo[2]+'/', '')
    f = open(destFolder+fileInfo[2]+'.txt','w')
    text = ''
 
    if (fileInfo[0] == 0):
        #rotate file if needed
        try:
            if rotate(pathToFile+fileInfo[2]+fileInfo[3]):
                print('Rotate file:', pathToFile+fileInfo[2]+fileInfo[3])
        except Exception as ex:
            logging('Try to rotate file ' + pathToFile+fileInfo[2]+fileInfo[3] + '. Except error: ' + str(ex))

        try:
            text = pytesseract.image_to_string(Image.open(pathToFile+fileInfo[2]+fileInfo[3]), lang='rus')
        except Exception as ex:
            logging('Try to convert file ' + pathToFile+fileInfo[2]+fileInfo[3] +' from image.' + ' Except error: ' + str(ex))
    else:
        for k in range(fileInfo[0]):
            try:
                if rotate(fileInfo[1]+fileInfo[2]+str(k)+fileInfo[3]):
                    print('Rotate file:', fileInfo[1]+fileInfo[2]+str(k)+fileInfo[3])
            except Exception as ex:
                logging('Try to rotate file ' + fileInfo[1]+fileInfo[2]+str(k)+fileInfo[3] + '. Except error: ' + str(ex))

        #get text from image
        try:
            for k in range(fileInfo[0]):
                text += pytesseract.image_to_string(Image.open(fileInfo[1]+fileInfo[2]+str(k)+fileInfo[3]), lang='rus')
        except Exception as ex:
            logging('Try to extract text from file ' + fileInfo[1]+fileInfo[2]+str(k)+fileInfo[3] +'.' + ' Except error: ' + str(ex))

    #write text to file
    try:
        f.write(text)
    except Exception as ex:
        logging('Try to write text to file ' + 'text/'+fileInfo[2]+'.txt' +'.' + ' Except error: ' + str(ex))
        return text

    f.close()

    try:
        print('')
        shutil.rmtree(fileInfo[1])
    except:
        print('Folder {} not found!'.format(fileInfo[1]))

    return pathToFile+fileInfo[2]+'.txt'

def convertTOtxt(dataFolder, destFolder, file):
   info = getFileInfo(dataFolder + file)

   if (path.exists(destFolder + info[1] + '.txt')):
     logging('File exist: ' + destFolder + info[1] + '.txt!' + '  skipping...')

   if (info[2].lower() == '.doc' or info[2].lower() == '.docx'):
     textFile = convertDoc2Txt(destFolder, dataFolder + file, info)
   else:
      if (info[2].lower() == '.pdf'):
        fileInfo = convertPDF2JPG(dataFolder + file)
        textFile = convertImageToText(destFolder, fileInfo)
      else:
        fileInfo = convertImageFile2JPG(dataFolder + file)
        textFile = convertImageToText(destFolder, fileInfo)

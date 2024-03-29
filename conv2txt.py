import os
from os import path
import cv2
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import shutil
import subprocess
import re
import time
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

text = ''

def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

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
    image = cv2.imread(imagePath, cv2.IMREAD_ANYCOLOR)
    orgAngle = int(re.search('(?<=Rotate: )\d+', pytesseract.image_to_osd(image)).group(0))
    if orgAngle != 0:
        angle=360-orgAngle
        (h, w) = image.shape[:2]
        if center is None:
            center = (w / 2, h / 2)
        # Perform the rotation
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))
        img = Image.fromarray(rotated, 'L')
        img.save(imagePath)
        return True

    return False

# convert file from doc or docx to text
def convertDoc2Txt(destFolder, path, info):
    text = ""
    if (info[2].lower() == '.doc'):
        flag = 1
        try:
          flag = subprocess.call(['soffice', '--headless', '--convert-to', 'docx', path, '--outdir', 'data/uploads'])
        except Exception as ex:
          logging('Try to convert and read DOC file ' + path + '. Except error: ' + str(ex))
        while flag == 1:
            time.sleep(0.5)
        doc = Document('data/uploads/'+info[1]+'.docx')
        while not os.path.exists('data/uploads/'+info[1]+'.docx'):
            time.sleep(0.5)
        while os.path.getsize('data/uploads/'+info[1]+'.docx') == 0:
            time.sleep(0.5)     
        if doc != '':
            text = ''
            for block in iter_block_items(doc):
                if isinstance(block, Paragraph):
                    text += ''.join(block.text)
                if isinstance(block, Table):
                    for i, row in enumerate(block.rows):
                        for i, cell in enumerate(row.cells):
                            if str(cell.text) != '':
                                if i != max(range(len(row.cells))):
                                   text += (str(cell.text) + ' - ')
                                else: 
                                    text += (str(cell.text) + '. ')
            f = open(destFolder+info[1]+'.txt','w')
            f.write(text)
            f.close()
    else:
        try:
            doc = Document(path)
            text = ''
            for block in iter_block_items(doc):
                if isinstance(block, Paragraph):
                    text += ''.join(block.text)
                if isinstance(block, Table):
                    for i, row in enumerate(block.rows):
                        for i, cell in enumerate(row.cells):
                            if str(cell.text) != '':
                                if i != max(range(len(row.cells))):
                                    text += (str(cell.text) + ' - ')
                                else: 
                                    text += (str(cell.text) + '. ')
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
   fileInfo = getFileInfo(path)
   try:
        os.mkdir(fileInfo[3])
   except:
        print("Folder exists!")
   images = convert_from_path(path, grayscale=True)
   for i, image in enumerate(images):
      image.save(fileInfo[3]+'/' +fileInfo[1]+str(i)+'.jpg', 'JPEG', quality=95)
   return (i, fileInfo[3]+'/', fileInfo[1], '.jpg')

#recognize image file and make text file
def convertImageToText(destFolder, fileInfo):
    pathToFile = fileInfo[1].replace(fileInfo[2]+'/', '')
    f = open(destFolder+fileInfo[2]+'.txt','w')
    text = ''
    if (fileInfo[0] == 0):
        #rotate file if needed
        try:
            if rotate(fileInfo[1]+fileInfo[2]+'0'+fileInfo[3]):
                print('Rotate file:', pathToFile+fileInfo[2]+'0'+fileInfo[3])
        except Exception as ex:
            logging('Try to rotate file ' + pathToFile+fileInfo[2]+'0'+fileInfo[3] + '. Except error: ' + str(ex))

        try:
            text = pytesseract.image_to_string(Image.open(fileInfo[1]+fileInfo[2]+'0'+fileInfo[3]), lang='rus', config='--psm 6 --oem 2')
        except Exception as ex:
            logging('Try to convert file ' + pathToFile+fileInfo[2]+'0'+fileInfo[3]+' from image.' + ' Except error: ' + str(ex))
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
                text += pytesseract.image_to_string(Image.open(fileInfo[1]+fileInfo[2]+str(k)+fileInfo[3]), lang='rus', config='--psm 6 --oem 2')
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

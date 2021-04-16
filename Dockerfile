FROM python:3.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN apt-get update
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y libsm6  
RUN apt-get install -y libxrender-dev
RUN apt-get install -y libxext6
RUN apt-get install -y libreoffice-core
RUN apt-get install -y poppler-utils
RUN apt-get install -y tesseract-ocr-eng 
RUN apt-get install -y tesseract-ocr-osd
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libtesseract-dev

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
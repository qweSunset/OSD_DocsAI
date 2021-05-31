FROM python:3.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

COPY rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata

RUN apt-get update
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y libsm6  
RUN apt-get install -y libxrender-dev
RUN apt-get install -y libxext6
RUN apt-get install -y libreoffice
RUN apt-get install -y libreoffice-writer
RUN apt-get install -y poppler-utils

RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libtesseract-dev
RUN apt-get install -y tesseract-ocr-eng 
RUN apt-get install -y tesseract-ocr-osd

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
ENV TF_XLA_FLAGS=--tf_xla_enable_xla_devices

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
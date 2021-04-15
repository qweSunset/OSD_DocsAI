FROM python:3.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y libsm6  
RUN apt-get install -y libxrender-dev
RUN apt-get install -y libxext6
RUN apt-get install -y libreoffice*

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
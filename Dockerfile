FROM thesheff17/chromelinuxbootstrapbase:latest

# time docker build . -t thesheff17/chromelinuxbootstrap:latest 

# this docker container is just a testing ground 
# to run this script on so its faster then testing on a chromebook
# technically you can use this script anywhere you want

# build date
RUN echo `date` > /root/build_date.txt

COPY ./bootstrap.py .
COPY ./gitinfo /root/gitinfo

RUN useradd -m dsheffner -s /bin/bash
RUN sudo ./bootstrap.py

CMD ["/bin/bash"]

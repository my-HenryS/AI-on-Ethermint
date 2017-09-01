FROM python:3

ADD ./ /build
WORKDIR /build/
RUN mkdir -p ~/.pip && mv pip.conf ~/.pip
RUN pip3 install -r requirements.txt


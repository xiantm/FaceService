FROM xinatm/face_recognization

#维护者信息
MAINTAINER xiantm xiantm@gmail.com

COPY . /root/face_service

WORKDIR /root/face_service

RUN chmod a+x boot.sh

RUN pip3 install -r requirements.txt

ENV FLASK_APP  face_service.py

EXPOSE 5000 80

ENTRYPOINT ["./boot.sh"]
FROM xiantm/face-recognization
COPY ./requirements.txt /opt
RUN pip3 install -r /opt/requirements.txt
# FROM c
# COPY . /opt/face_service
# WORKDIR /opt/face_service
# RUN chmod a+x boot.sh
# ENV FLASK_APP  manage.py
# EXPOSE 5000 80
# ENTRYPOINT ["./boot.sh"]
from app import db


"""人脸信息
"""


class Face(db.Model):

    __tablename__='ticket_img_info'

    image_id = db.Column(db.Integer,primary_key=True)
    sold_id = db.Column(db.Integer)
    sold_chip = db.Column(db.String(40))
    sold_code = db.Column(db.String(40))
    sold_face_photo = db.Column(db.String(200))
    sold_user_name  = db.Column(db.String(40))
    project_id = db.Column(db.String(40))
    face_encode = db.Column(db.TEXT)
    faces = []
    def __repr__(self):
        return '<Face {}>'.format(self.sold_id)
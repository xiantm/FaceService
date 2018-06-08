from app import db


"""人脸信息
"""


class Face(db.Model):

    __tablename__='ticket_sold'

    sold_id = db.Column(db.Integer,primary_key=True)
    sold_chip = db.Column(db.String(40))
    sold_face_photo = db.Column(db.String(200))
    sold_user_name  = db.Column(db.String(40))
    ticket_project_id = db.Column(db.String(40))
    face_encode = db.Column(db.TEXT)
    faces = []
    def __repr__(self):
        return '<Face {}>'.format(self.sold_id)
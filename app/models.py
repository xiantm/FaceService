from app import db


class Face(db.Model):
    """人脸信息
    """
    __tablename__ = 'face'
    id = db.Column(db.Integer, primary_key=True)
    face_encode = db.Column(db.TEXT)
    name = db.Column(db.String(40))
    create_time = db.Column(db.DateTime)
    group_id = db.Column(db.Integer)
    face_size = db.Column(db.Integer)
    file_name = db.Column(db.String(80))
    faces = []

    def __repr__(self):
        return '<Face {}>'.format(self.id)


class Group(db.Model):
    __tablename__ = "face_group"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))

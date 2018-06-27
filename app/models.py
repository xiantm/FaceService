from app import db


class Face(db.Model):
    """人脸信息
    """
    __tablename__ = 'face'
    id = db.Column(db.String(50), autoincrement=False, primary_key=True)
    face_encode = db.Column(db.TEXT)
    create_time = db.Column(db.DateTime)
    group_id = db.Column(db.String(200))
    face_url = db.Column(db.String(500), nullable=True)
    face_size = db.Column(db.Integer)
    faces = []

    def __repr__(self):
        return '<Face {}>'.format(self.id)

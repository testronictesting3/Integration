from extesnsions.database import db

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Parameter model: {self.parameter}, created at {self.date_created}"

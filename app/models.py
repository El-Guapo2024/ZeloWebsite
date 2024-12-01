# from app import db
# from datetime import datetime


# class Bike(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     type = db.Column(db.String(20))
#     last_maintenance = db.Column(db.DateTime)
#     status = db.Column(db.String(20), default='active')

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'type': self.type,
#             'last_maintenance': self.last_maintenance.strftime('%Y-%m-%d') if self.last_maintenance else None,
#             'status': self.status
#         }
# TODO use model method to interface with the databae 

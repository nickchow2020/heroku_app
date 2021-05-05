from modals import Feedbacks,db,User
from app import app

db.drop_all()
db.create_all()


user1 = User.register(
    username="shuminzhou",
    password="shuminzhou",
    email="smz1234@gmail.com",
    first="Nick",
    last="Zhou")

user2 = User.register(
    username="nick123",
    password="shuminzhou",
    email="smz12234@gmail.com",
    first="Stephen",
    last="Zhou")


db.session.add(user1)
db.session.add(user2)
db.session.commit()


tweet1 = Feedbacks(title="Hello,World",content="I Love You",username="shuminzhou")
tweet2 = Feedbacks(title="Thank Your,World",content="I Love You",username="shuminzhou")
tweet3 = Feedbacks(title="Okay,World",content="I Love You",username="nick123")
tweet4 = Feedbacks(title="Lucky,World",content="I Love You",username="nick123")

db.session.add(tweet1)
db.session.add(tweet2)
db.session.add(tweet3)
db.session.add(tweet4)

db.session.commit()
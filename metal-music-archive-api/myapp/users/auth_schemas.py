from ninja import Schema



class RegisterIn(Schema):
    username: str
    password: str

class RegisterOut(Schema):
    id: int
    username: str

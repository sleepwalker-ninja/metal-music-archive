from ninja import Router
from .auth_schemas import RegisterIn, RegisterOut
from myapp.models import User
from ninja.errors import HttpError
import logging
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth


logger = logging.getLogger(__name__)

router = Router(tags=["Auth"])

@router.post("/register", response=RegisterOut)
def create_user(request, data: RegisterIn):
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username already exist")
    
    user = User.objects.create_user(
        username=data.username,
        password=data.password
    )
    
    return user

# @router.delete("/delete-user/{user_id}")
# def delete_user(request, user_id: int):
#     user = get_object_or_404(User, id=user_id)
#     user.delete()
    
#     return {"message": "success"}
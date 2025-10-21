from django.contrib.auth import get_user_model

User = get_user_model()

class UserService:

    @staticmethod
    def create_user(email, password, name):
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

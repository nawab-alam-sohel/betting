from django.contrib.auth import get_user_model

User = get_user_model()

class UserService:

    @staticmethod
    def create_user(email, password, name):
        # The User model uses `full_name`; accept `name` from APIs and map to `full_name`.
        user = User(email=email, full_name=name)
        user.set_password(password)
        user.save()
        return user

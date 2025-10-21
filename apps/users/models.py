from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class Role(models.Model):
    """
    Dynamic role model.
    - name: display name
    - slug: unique short key (eg. superadmin, admin, agent, user)
    - level: integer to indicate hierarchy (higher => more power)
    - parent: optional FK to define parent role
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    level = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children")

    class Meta:
        ordering = ["-level", "name"]

    def __str__(self):
        return f"{self.name} ({self.slug})"

# --- Your existing UserManager here (keep as-is) ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # Replace old role CharField with FK to Role
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # helper method to check role/hierarchy
    def has_role(self, slug):
        """
        check if user has role with slug
        """
        if not self.role:
            return False
        return self.role.slug == slug

    def has_minimum_role_level(self, level):
        """
        Return True if user's role level >= required level
        """
        if not self.role:
            return False
        return self.role.level >= level

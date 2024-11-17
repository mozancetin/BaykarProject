from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db import models

# Bu dosyada projemiz için gerekli olan sınıfları tanımlıyoruz.

# Djangonun kendi User modelini modifiye edip kendi alanlarımı eklemek istediğim için yeni bir CustomUser sınıfı ve bu sınıfın
# ..işlemlerini yapmak için CustomUserManager sınıfını oluşturdum.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user : CustomUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Takım tiplerini ve kısaltmalarını belirledim.
    TEAM_TYPES = [
        ("Kanat", "Kanat Takımı"),
        ("Gövde", "Gövde Takımı"),
        ("Kuyruk", "Kuyruk Takımı"),
        ("Aviyonik", "Aviyonik Takımı"),
        ("Montaj", "Montaj Takımı")
    ]

    # Kullanıcak alanları belirledim.
    email = models.EmailField(unique=True, blank = False, null = False)
    full_name = models.CharField(max_length=100, blank = False, null = False)
    team_type = models.CharField(max_length=8, choices = TEAM_TYPES, blank = False, null = False)
    age = models.PositiveIntegerField(blank = False, null = False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'team_type', 'age']

    # ./api/serializers.py dosyasında kullandığımız tam takım adını veren fonksiyon.
    def get_full_team_type(self):
        return dict(self.TEAM_TYPES).get(self.team_type, self.team_type)

class Plane(models.Model):
    # Uçak tiplerini ve kısaltmalarını belirledim
    PLANE_TYPES = [
        ("TB2", "TB2"),
        ("TB3", "TB3"),
        ("AKI", "AKINCI"),
        ("KIZ", "KIZILELMA")
    ]

    # Uçak modeli için kullanılacak alanları belirledim
    plane_type = models.CharField(max_length = 3, choices = PLANE_TYPES, blank = False, null = False, verbose_name="Uçak Tipi")
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Personel", blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ./api/serializers.py dosyasında kullandığımız tam uçak tipini veren fonksiyon.
    def get_full_plane_type(self):
        return dict(self.PLANE_TYPES).get(self.plane_type, self.plane_type)

class Part(models.Model):
    # Parça tiplerini ve kısaltmalarını belirledim
    PART_TYPES = [
        ("Kanat", "Kanat"),
        ("Gövde", "Gövde"),
        ("Kuyruk", "Kuyruk"),
        ("Aviyonik", "Aviyonik")
    ]

    # Parça modeli için kullanılacak alanları belirledim
    part_type = models.CharField(max_length = 8, choices = PART_TYPES, blank = False, null = False, verbose_name="Parça Tipi")
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, verbose_name="Uçak", blank=True, null=True)
    plane_type = models.CharField(max_length = 3, choices = Plane.PLANE_TYPES, blank = False, null = False, verbose_name="Uçak Tipi")
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Personel", blank = False, null = False)
    mounted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ./api/serializers.py dosyasında kullandığımız tam uçak tipini veren fonksiyon.
    def get_full_plane_type(self):
        return dict(Plane.PLANE_TYPES).get(self.plane_type, self.plane_type)

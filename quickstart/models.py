import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from tutorial.logging import logger


# get_file_path позволяет сохранять файлы с уникальными именами в определенной папке
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/products', filename)


# models here.
class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Product(Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True, )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)

    # В этом примере, я добавил вызов logger.info в метод save модели Product. Каждый раз, когда продукт сохраняется,
    # сообщение будет записано в журнал.
    def save(self, *args, **kwargs):
        logger.info('Saving product: %s', self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = 'Products'


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    # create_user() принимает email и password и создает и сохраняет пользователя с заданными данными.
    # normalize_email() преобразует доменное имя в нижний регистр.
    # set_password() преобразует пароль в хэш.
    # save() сохраняет пользователя в базе данных.

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)
    # create_superuser() принимает email и password и создает и сохраняет пользователя с заданными данными.
    # extra_fields.setdefault() устанавливает значения по умолчанию для is_staff, is_superuser и is_active.
    # Если is_staff и is_superuser не установлены в True, то возникает исключение.
    # Если is_staff и is_superuser установлены в True, то вызывается метод create_user().


class UserData(AbstractUser):
    username = None
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class WishList(Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self) -> str:
        return self.user.name + " wishlist"

    class Meta:
        verbose_name_plural = 'WishLists'

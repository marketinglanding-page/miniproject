from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
# users/models.py

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일이 필요합니다')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # Django의 기본 username 필드를 사용하지 않고 email을 USERNAME_FIELD로 설정
    username = None

    email = models.EmailField(verbose_name="이메일", max_length=100, unique=True)
    name = models.CharField(verbose_name="이름", max_length=50)
    nickname = models.CharField(verbose_name="닉네임", max_length=50, unique=True)
    phone_number = models.CharField(verbose_name="전화번호", max_length=20, blank=True, null=True)

    # is_superuser, is_active, last_login 등은 AbstractUser가 제공
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일", auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname']

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'

    def __str__(self):
        return self.email

class TokenBlacklist(models.Model):
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='token_blacklist',
    #     verbose_name="사용자"
    # )
    token = models.CharField(verbose_name="토큰", max_length=512, unique=True)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        db_table = 'token_blacklist'
        verbose_name = '토큰 블랙리스트'
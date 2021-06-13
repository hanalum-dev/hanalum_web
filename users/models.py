"""사용자 계정 모델(user)을 정의하는 파일입니다."""
from datetime import datetime

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.templatetags.static import static


class UserManager(BaseUserManager):
    """ 클래스를 관리하는 클래스"""

    def _create_user(self, email, password=None, **kwargs):
        """사용자 생성 protected 메소드"""
        if not email:
            raise ValueError("이메일은 필수입니다")
        user = self.model(
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password=None, **kwargs):
        """사용자 생성 public 메소드"""
        kwargs.setdefault("is_admin", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password=None, **kwargs):
        """슈퍼 유저(superuser) 생성 메소드"""
        kwargs.setdefault("is_admin", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """유저 클래스 (DB 생성)"""

    GENDER_CHOICES = (("M", "남"), ("F", "여"), ("E", "기타"), ("X", "선택안함"))

    USER_CATEGORY_CHOICES = []
    for year in range(2014, datetime.today().year + 1):
        category = "{}({}기)".format(year, year - 2013)
        USER_CATEGORY_CHOICES.append((category, category))

    USER_CATEGORY_CHOICES.append(("교직원", "교직원"))
    USER_CATEGORY_CHOICES.append(("외부인", "외부인"))
    USER_CATEGORY_CHOICES.append(("한아름", "한아름"))
    USER_CATEGORY_CHOICES.append(("관리자", "관리자"))
    USER_CATEGORY_CHOICES = tuple(USER_CATEGORY_CHOICES)

    email = models.EmailField(
        verbose_name="이메일",
        max_length=255,
        unique=True,
    )
    nickname = models.TextField(
        verbose_name="닉네임",
    )
    realname = models.CharField(
        verbose_name="이름",
        max_length=10,
    )
    gender = models.CharField(
        verbose_name="성별",
        max_length=1,
        choices=GENDER_CHOICES,
    )
    read_authority = models.IntegerField(
        verbose_name="읽기 권한",
        default=1,
    )
    write_authority = models.IntegerField(
        verbose_name="작성 권한",
        default=0,
    )
    avatar = models.ImageField(
        verbose_name="아바타",
        upload_to="avatars/",
        null=True,
        blank=True,
    )
    user_category = models.CharField(
        verbose_name="유저 카테고리",
        max_length=10,
        choices=USER_CATEGORY_CHOICES,
    )
    created_at = models.DateTimeField(
        verbose_name="created_at",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="updated_at",
        auto_now=True
    )
    is_active = models.BooleanField(
        verbose_name="Is active",
        default=True,
    )
    is_admin = models.BooleanField(
        verbose_name="Is admin",
        default=False,
    )
    is_staff = models.BooleanField(
        verbose_name="Is staff",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="Is superuser",
        default=False,
    )
    roles = models.TextField(
        default="",
        null=False,
        blank=True,
        verbose_name="roles"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "realname", "gender", "user_category"]

    def __str__(self):
        """user 객체 -> str"""
        return "{}".format(self.nickname)

    @property
    def avatar_image_url(self):
        """유저의 아바타 이미지 url helper"""
        if self.avatar:
            return self.avatar.url  # pylint: disable=E1101
        return static('img/no-title-logo.png')

    @property
    def is_hanmaum_member(self):
        return 'hanmaum' in self.roles

    @property
    def is_joha_chief(self):
        return 'joha_chief' in self.roles

    @property
    def is_joha_editor(self):
        return 'joha_editor' in self.roles

    @property
    def is_joha_reviewer(self):
        return 'joha_reviewer' in self.roles

    class Meta:
        """user meta class"""

        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("-updated_at",)

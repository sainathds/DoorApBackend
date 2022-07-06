from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class MyCustomManager(BaseUserManager):
	def _create_user(self, name, email, password,is_staff, is_superuser, firebase_token, is_vendor, is_customer, created_datime, login_type, login_id, **extra_fields):
		if not email:
			raise ValueError('Users must have email...')

		now = timezone.now()

		email = email
		user = self.model(
			name=name,
			email=email,
			is_staff=is_staff,
			firebase_token=firebase_token, 
			is_superuser=is_superuser, 
			is_vendor=is_vendor, 
			is_customer=is_customer, 
			last_login=now,
			created_datime=now,
			login_type=login_type,
			login_id=login_id,
			**extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		user=self._create_user("", email, password, True, True, "", False, False, None, "", "", **extra_fields)
		return user
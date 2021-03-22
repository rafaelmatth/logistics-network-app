from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


    def create_customer(self, email, password=None, **extra_fields):
        """
        Create and save a Customer with the given email, password and profile.
        """
        extra_fields.setdefault('is_customer', True)

        birth_date = extra_fields.pop('birth_date', None)
        cpf = extra_fields.pop('cpf', None)
        phone = extra_fields.pop('phone', None)

        if extra_fields.get('is_customer') is not True:
            raise ValueError('Customer must have is_customer=True.')
        if not cpf:
            raise ValueError('The given cpf must be set.')
        if not phone:
            raise ValueError('The given phone must be set.')

        user = self._create_user(email, password, **extra_fields)

        from apps.account.models import Profile
        Profile.objects.create(
            user=user, cpf=cpf, phone=phone, birth_date=birth_date)

        return user
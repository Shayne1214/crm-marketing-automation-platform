from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class Account(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    main_email = models.EmailField(blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['main_email']),
        ]

    def __str__(self):
        return self.name


class Lead(models.Model):
    STATUS_CHOICES = [
        ('unused', 'Unused'),
        ('sent', 'Sent'),
        ('bad', 'Bad'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('replied', 'Replied'),
        ('demoed', 'Demoed'),
    ]

    Email = models.EmailField(db_column='email', db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unused', db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['Email']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.Email


class Email(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='emails')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'emails'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.email


class MessageTemplate(models.Model):
    content = models.TextField()
    industry = models.CharField(max_length=255, blank=True, db_index=True)
    skills = models.JSONField(default=list, blank=True)
    used = models.IntegerField(default=0)
    replied = models.IntegerField(default=0)
    succeeded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'message_templates'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['industry']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Message Template {self.id}"


class SubjectTemplate(models.Model):
    content = models.CharField(max_length=500)
    used = models.IntegerField(default=0)
    replied = models.IntegerField(default=0)
    succeeded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subject_templates'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.content


# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    firebase_uid = models.CharField(
        max_length=255, unique=True, primary_key=True)
    is_premium = models.BooleanField(default=False, help_text=_("Designates whether the user has premium subscription"),
                                     )
    # Additional custom fields (if any)
    '''
    CustomUser model is clashing with Django's built-in User model regarding the groups and user_permissions relationships. When you extend AbstractUser, Django tries to create reverse relationships for groups and user_permissions, but these clash with those already defined in the default User model.

    To resolve this, you need to set the related_name attribute for both groups and user_permissions in your CustomUser model. This tells Django to use a different name for the reverse relationship.
    '''
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    # Override the groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        # provides a unique name for the reverse relation from Group and Permission to CustomUser.
        related_name="customuser_set",
        # is used to name the reverse filter name from Group and Permission.
        related_query_name="customuser",
    )

    # Override the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )


class CreditAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    last_updated = models.DateTimeField(default=now)

# Payment Transaction Model


class PaymentTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=100, default='unknown')
    payment_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=100, default='pending')

# Credit Transaction Model


class CreditTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    transaction_type = models.CharField(max_length=100, default='unknown')
    transaction_date = models.DateTimeField(default=now)

# Subscription Model


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(default=now)
    subscription_type = models.CharField(max_length=100, default='monthly')
    status = models.CharField(max_length=100, default='active')

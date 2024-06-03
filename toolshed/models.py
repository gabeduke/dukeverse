from django.db import models
from django.contrib.auth.models import User

class Tool(models.Model):
    TOOL_TYPE_CHOICES = [
        ('Electric', 'Electric'),
        ('Battery', 'Battery'),
        ('Manual', 'Manual'),
    ]

    name = models.CharField(max_length=255)
    tool_type = models.CharField(max_length=50, choices=TOOL_TYPE_CHOICES)
    battery = models.CharField(max_length=50, blank=True, null=True)
    custodian = models.ForeignKey(User, related_name='custodian_tools', on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255)
    is_checked_out = models.BooleanField(default=False)
    checked_out_by = models.ForeignKey(User, related_name='checked_out_tools', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, related_name='assigned_tools', on_delete=models.SET_NULL, null=True, blank=True)


def __str__(self):
        return self.name

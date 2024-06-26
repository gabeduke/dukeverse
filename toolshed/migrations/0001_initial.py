# Generated by Django 5.0.6 on 2024-06-01 03:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('tool_type', models.CharField(choices=[('Electric', 'Electric'), ('Battery', 'Battery'), ('Manual', 'Manual')], max_length=50)),
                ('battery', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(max_length=255)),
                ('is_checked_out', models.BooleanField(default=False)),
                ('checked_out_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checked_out_tools', to=settings.AUTH_USER_MODEL)),
                ('custodian', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custodian_tools', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-03 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_customuser_is_premium"),
    ]

    operations = [
        migrations.RemoveField(model_name="userasset", name="user",),
        migrations.DeleteModel(name="Game",),
        migrations.DeleteModel(name="UserAsset",),
    ]

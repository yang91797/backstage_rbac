# Generated by Django 2.0.3 on 2020-06-28 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='URL别名'),
        ),
    ]
# Generated by Django 4.0.2 on 2022-04-12 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_currency_customuser_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.currency'),
        ),
    ]
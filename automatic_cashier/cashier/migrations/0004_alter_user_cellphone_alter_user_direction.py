# Generated by Django 4.2.6 on 2023-10-16 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0003_alter_account_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(default='not apply', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='direction',
            field=models.TextField(default='not apply'),
        ),
    ]

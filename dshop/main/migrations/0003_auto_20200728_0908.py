# Generated by Django 3.0.8 on 2020-07-28 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200726_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='is_active',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Активация'),
        ),
    ]

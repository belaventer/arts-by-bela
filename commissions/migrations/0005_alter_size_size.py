# Generated by Django 3.2.6 on 2021-08-20 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0004_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(choices=[('210 x 297 mm', 'A4'), ('148 x 210 mm', 'A5'), ('105 x 148 mm', 'A6'), ('74 x 105 mm', 'A7')], default='105 x 148 mm', max_length=12, unique=True),
        ),
    ]

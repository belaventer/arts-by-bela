# Generated by Django 3.2.6 on 2021-09-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0009_auto_20210904_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wip',
            name='client_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]

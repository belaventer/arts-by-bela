# Generated by Django 3.2.6 on 2021-09-02 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0007_commission'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='reference_image_five',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='commission',
            name='reference_image_four',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='commission',
            name='reference_image_one',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='commission',
            name='reference_image_three',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='commission',
            name='reference_image_two',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
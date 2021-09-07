# Generated by Django 3.2.6 on 2021-09-07 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0010_alter_wip_client_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_review', models.TextField(blank=True, null=True)),
                ('final_illustration', models.ImageField(blank=True, null=True, upload_to='')),
                ('commission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='artwork', to='commissions.commission')),
            ],
        ),
    ]

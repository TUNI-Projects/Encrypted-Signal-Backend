# Generated by Django 4.1.7 on 2023-05-09 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0005_filemodel_encrypted_data_alter_filemodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='encrypted_data',
            field=models.TextField(blank=True),
        ),
    ]

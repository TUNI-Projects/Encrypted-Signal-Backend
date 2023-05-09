# Generated by Django 4.1.7 on 2023-05-09 19:58

from django.db import migrations, models
import share.models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0007_alter_filemodel_encrypted_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file',
            field=models.FileField(blank=True, upload_to=share.models.update_filename, validators=[share.models.validate_file_size]),
        ),
    ]

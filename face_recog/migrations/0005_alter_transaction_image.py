# Generated by Django 4.2.5 on 2024-02-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("face_recog", "0004_alter_transaction_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="Image",
            field=models.ImageField(upload_to=""),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-03 03:01

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_alter_fatura_is_a_vista"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fatura",
            name="arquivo",
            field=models.FileField(
                upload_to="faturas/", validators=[main.validators.validar_extensao]
            ),
        ),
    ]

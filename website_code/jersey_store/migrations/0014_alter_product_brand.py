# Generated by Django 5.0 on 2023-12-27 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jersey_store', '0013_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, choices=[('Nike', 'Nike'), ('Adidas', 'Adidas'), ('Champion', 'Champion'), ('New Balance', 'New Balance'), ('Tommy Hilfiger', 'Tommy Hilfiger'), ('Puma', 'Puma'), ('Reebok', 'Reebok')], max_length=50, null=True),
        ),
    ]

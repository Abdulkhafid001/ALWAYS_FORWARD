# Generated by Django 5.0 on 2023-12-27 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jersey_store', '0012_remove_order_created_remove_order_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, choices=[('Nike', 'Jersey'), ('Adidas', 'Boots'), ('Champion', 'Accessories'), ('New Balance', 'Accessories'), ('Tommy Hilfiger', 'Accessories'), ('Puma', 'Accessories'), ('Reebok', 'Accessories')], max_length=50, null=True),
        ),
    ]

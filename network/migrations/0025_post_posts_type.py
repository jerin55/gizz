# Generated by Django 4.1.3 on 2022-12-08 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0024_alter_cart_product_alter_post_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='posts_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

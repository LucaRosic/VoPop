# Generated by Django 4.2.14 on 2024-08-30 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_product_unique_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="product_summary",
            name="negative_count",
            field=models.DecimalField(decimal_places=0, default=100, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product_summary",
            name="postive_count",
            field=models.DecimalField(decimal_places=0, default=100, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product_summary",
            name="review_count",
            field=models.DecimalField(decimal_places=0, default=100, max_digits=5),
            preserve_default=False,
        ),
    ]
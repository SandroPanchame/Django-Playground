# Generated by Django 5.0.3 on 2024-04-05 23:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_alter_collection_featured_product_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
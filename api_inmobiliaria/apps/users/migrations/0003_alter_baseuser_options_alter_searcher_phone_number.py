# Generated by Django 5.1.1 on 2024-09-07 17:42

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_baseuser_table_alter_searcher_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="baseuser",
            options={
                "verbose_name": "Base user",
                "verbose_name_plural": "Base users",
            },
        ),
        migrations.AlterField(
            model_name="searcher",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                db_column="phone_number",
                max_length=19,
                null=True,
                region=None,
                unique=True,
            ),
        ),
    ]
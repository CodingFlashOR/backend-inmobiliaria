# Generated by Django 5.1.1 on 2024-09-24 00:34

import apps.users.models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="RealEstateEntity",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        db_column="uuid",
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "type_entity",
                    models.CharField(
                        choices=[
                            ("realestate", "realestate"),
                            ("constructioncompany", "constructioncompany"),
                        ],
                        db_column="type_entity",
                        max_length=40,
                    ),
                ),
                ("logo", models.CharField(db_column="logo", max_length=2083)),
                (
                    "name",
                    models.CharField(
                        db_column="name", db_index=True, max_length=40, unique=True
                    ),
                ),
                (
                    "description",
                    models.CharField(db_column="description", max_length=400),
                ),
                (
                    "nit",
                    models.CharField(
                        db_column="nit", db_index=True, max_length=10, unique=True
                    ),
                ),
                (
                    "phone_numbers",
                    models.CharField(
                        db_column="phone_numbers", db_index=True, max_length=39
                    ),
                ),
                (
                    "department",
                    models.CharField(
                        db_column="department", db_index=True, max_length=25
                    ),
                ),
                (
                    "municipality",
                    models.CharField(
                        db_column="municipality", db_index=True, max_length=25
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        db_column="region", db_index=True, max_length=80
                    ),
                ),
                (
                    "coordinate",
                    models.CharField(
                        db_column="coordinate",
                        db_index=True,
                        max_length=30,
                        unique=True,
                    ),
                ),
                (
                    "is_phones_verified",
                    models.JSONField(db_column="is_phones_verified"),
                ),
                (
                    "communication_channels",
                    models.JSONField(db_column="communication_channels"),
                ),
                (
                    "documents",
                    models.JSONField(blank=True, db_column="documents", null=True),
                ),
                ("verified", models.BooleanField(db_column="verified")),
            ],
            options={
                "verbose_name": "Real Estate Entity",
                "verbose_name_plural": "Real Estate Entities",
            },
        ),
        migrations.CreateModel(
            name="Searcher",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        db_column="uuid",
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_column="name", max_length=40)),
                (
                    "last_name",
                    models.CharField(db_column="last_name", max_length=40),
                ),
                (
                    "cc",
                    models.CharField(
                        blank=True,
                        db_column="cc",
                        db_index=True,
                        max_length=10,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        db_column="phone_number",
                        db_index=True,
                        max_length=19,
                        null=True,
                        region=None,
                        unique=True,
                    ),
                ),
                (
                    "is_phone_verified",
                    models.BooleanField(db_column="is_phone_verified"),
                ),
            ],
            options={
                "verbose_name": "Searcher",
                "verbose_name_plural": "Searchers",
            },
        ),
        migrations.CreateModel(
            name="BaseUser",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        db_column="uuid",
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_column="email",
                        db_index=True,
                        max_length=40,
                        unique=True,
                    ),
                ),
                (
                    "password",
                    models.CharField(db_column="password", max_length=128),
                ),
                (
                    "role_data_uuid",
                    models.UUIDField(
                        blank=True, db_column="role_data_uuid", null=True
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(db_column="is_staff", default=False),
                ),
                (
                    "is_superuser",
                    models.BooleanField(db_column="is_superuser", default=False),
                ),
                (
                    "is_active",
                    models.BooleanField(db_column="is_active", default=False),
                ),
                (
                    "is_deleted",
                    models.BooleanField(db_column="is_deleted", default=False),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, db_column="deleted_at", null=True
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, db_column="last_login", null=True
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        auto_now_add=True, db_column="date_joined"
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        db_column="content_type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Base user",
                "verbose_name_plural": "Base users",
                "indexes": [
                    models.Index(
                        fields=["uuid", "is_active"],
                        name="users_baseu_uuid_c1d390_idx",
                    )
                ],
            },
            managers=[
                ("objects", apps.users.models.UserManager()),
            ],
        ),
    ]

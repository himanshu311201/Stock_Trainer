# Generated by Django 4.1.2 on 2022-10-26 12:26

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Consultant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "consultant_name",
                    models.CharField(
                        max_length=30,
                        validators=[django.core.validators.MinLengthValidator(5)],
                    ),
                ),
                ("consultant_rating", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image_field", models.ImageField(upload_to="Images")),
                ("rating", models.FloatField(default=0.0)),
                ("consultant", models.BooleanField(default=False)),
                ("about_me", models.TextField(default="")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subscribe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.TimeField()),
                (
                    "meet_id",
                    models.CharField(
                        max_length=50,
                        validators=[django.core.validators.MinLengthValidator(10)],
                    ),
                ),
                (
                    "reg_consultant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="User.consultant",
                    ),
                ),
                (
                    "reg_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="User.profile"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="consultant",
            name="consultant_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Consultant",
                to="User.profile",
            ),
        ),
        migrations.CreateModel(
            name="Blogs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                (
                    "blogs",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name=""
                    ),
                ),
                (
                    "date_posted",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog",
                        to="User.consultant",
                    ),
                ),
                (
                    "upvotes",
                    models.ManyToManyField(
                        related_name="upv", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
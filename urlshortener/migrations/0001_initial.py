# Generated by Django 4.1.5 on 2023-01-14 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="InvalidREDIRECT",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("txID", models.CharField(blank=True, max_length=100, null=True)),
                ("uri", models.CharField(blank=True, max_length=2048, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Landing_HIT",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                ("hit_count", models.IntegerField(default=1)),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-date",),},
        ),
        migrations.CreateModel(
            name="Login_Session",
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
                ("user", models.CharField(blank=True, max_length=150, null=True)),
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="NormalURL",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("txID", models.CharField(blank=True, max_length=100, null=True)),
                ("user", models.CharField(blank=True, max_length=250, null=True)),
                ("inputURL", models.CharField(blank=True, max_length=2048, null=True)),
                ("outputURL", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-date",),},
        ),
        migrations.CreateModel(
            name="ShortenedURL",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("txID", models.CharField(blank=True, max_length=100, null=True)),
                ("user", models.CharField(blank=True, max_length=250, null=True)),
                ("inputURL", models.CharField(blank=True, max_length=2048, null=True)),
                ("outputURL", models.CharField(blank=True, max_length=25, null=True)),
                ("hitcount", models.IntegerField(default=0)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                ("type_of_url", models.CharField(blank=True, max_length=13, null=True)),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-hitcount",),},
        ),
        migrations.CreateModel(
            name="UnregisteredUser",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("txID", models.CharField(blank=True, max_length=100, null=True)),
                ("user", models.CharField(blank=True, max_length=150, null=True)),
                ("inputURL", models.CharField(blank=True, max_length=2048, null=True)),
                ("outputURL", models.CharField(blank=True, max_length=25, null=True)),
                ("hitcount", models.IntegerField(default=0)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "type_of_url",
                    models.CharField(
                        blank=True, default="Normal", max_length=13, null=True
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-date",),},
        ),
        migrations.CreateModel(
            name="User_limit",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("user", models.CharField(blank=True, max_length=150, null=True)),
                ("url_count", models.IntegerField(default=0)),
                ("last_update", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Visitor",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("txID", models.CharField(blank=True, max_length=100, null=True)),
                ("user", models.CharField(blank=True, max_length=250, null=True)),
                ("inputURL", models.CharField(blank=True, max_length=2048, null=True)),
                ("outputURL", models.CharField(blank=True, max_length=25, null=True)),
                ("type_of_url", models.CharField(blank=True, max_length=13, null=True)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-date",),},
        ),
        migrations.CreateModel(
            name="Userprofile",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("brand_name", models.CharField(blank=True, max_length=250, null=True)),
                ("email", models.EmailField(max_length=254)),
                ("subscribed", models.BooleanField(default=False)),
                (
                    "subscription_plan",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Free", "Free"),
                            ("Basic", "Basic"),
                            ("Premium", "Premium"),
                            ("Enterprise", "Enterprise"),
                        ],
                        default="Free",
                        max_length=10,
                        null=True,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("-date",),},
        ),
        migrations.CreateModel(
            name="RegisteredUser",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("txID", models.CharField(blank=True, max_length=100, null=True)),
                ("inputURL", models.CharField(blank=True, max_length=2048, null=True)),
                ("outputURL", models.CharField(blank=True, max_length=2048, null=True)),
                ("hitcount", models.IntegerField(default=0)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                ("type_of_url", models.CharField(blank=True, max_length=13, null=True)),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("-date",),},
        ),
        migrations.CreateModel(
            name="CustomizedURL",
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
                ("ip", models.CharField(blank=True, max_length=25, null=True)),
                ("txID", models.CharField(blank=True, max_length=100, null=True)),
                ("inputURL", models.CharField(blank=True, max_length=2048, null=True)),
                ("outputURL", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "type_of_device",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("deviceName", models.CharField(blank=True, max_length=50, null=True)),
                ("deviceOS", models.CharField(blank=True, max_length=50, null=True)),
                ("browser", models.CharField(blank=True, max_length=50, null=True)),
                ("location", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_state", models.CharField(blank=True, max_length=125, null=True)),
                ("loc_city", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("-date",),},
        ),
    ]
# Generated by Django 3.0.5 on 2020-04-15 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chrisapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Punchline",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("punchline_text", models.CharField(max_length=200)),
                ("likes", models.IntegerField(default=0)),
                (
                    "joke",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chrisapp.Joke"
                    ),
                ),
            ],
        ),
    ]

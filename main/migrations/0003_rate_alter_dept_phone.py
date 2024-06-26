# Generated by Django 5.0.6 on 2024-05-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField(default=0)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='dept',
            name='phone',
            field=models.CharField(max_length=13),
        ),
    ]

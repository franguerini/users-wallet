# Generated by Django 3.2.12 on 2022-02-12 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserWalletsApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('alias', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Departments',
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-26 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='(empty)', max_length=55)),
                ('manager', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Hook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='(empty)', max_length=30)),
                ('url', models.CharField(max_length=150, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line_bot.group')),
            ],
        ),
    ]

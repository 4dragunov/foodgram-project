# Generated by Django 3.1.7 on 2021-02-19 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients_for_recipe',
            name='amount',
            field=models.PositiveIntegerField(default=1, help_text='в граммах'),
        ),
    ]

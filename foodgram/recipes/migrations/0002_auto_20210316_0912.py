# Generated by Django 3.1.7 on 2021-03-16 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients_for_recipe',
            new_name='IngredientsForRecipe',
        ),
    ]

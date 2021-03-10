# Generated by Django 3.1.7 on 2021-03-01 07:01

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20210228_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('breakfast', 'breakfast'), ('lunch', 'lunch'), ('dinner', 'dinner')], default='breakfast', max_length=22, verbose_name='Теги'),
        ),
    ]

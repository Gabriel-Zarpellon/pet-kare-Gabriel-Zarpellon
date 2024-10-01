# Generated by Django 5.1.1 on 2024-10-01 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '006_alter_pet_sex'),
        ('traits', '0002_trait_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='traits',
            field=models.ManyToManyField(related_name='traits', to='traits.trait'),
        ),
    ]

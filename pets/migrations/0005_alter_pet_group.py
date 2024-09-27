# Generated by Django 5.1.1 on 2024-09-27 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_remove_group_pets'),
        ('pets', '0004_pet_group_alter_pet_traits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pets', to='groups.group'),
        ),
    ]

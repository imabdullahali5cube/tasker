# Generated by Django 4.2.7 on 2023-11-15 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('developers', '0006_alter_project_developer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='developer',
        ),
        migrations.AddField(
            model_name='project',
            name='developers',
            field=models.ManyToManyField(to='developers.developers'),
        ),
    ]

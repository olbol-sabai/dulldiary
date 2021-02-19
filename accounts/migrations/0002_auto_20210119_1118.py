# Generated by Django 3.1.5 on 2021-01-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='appreciated_entries',
            field=models.ManyToManyField(related_name='appreciated', to='entries.Entry'),
        ),
        migrations.AddField(
            model_name='user',
            name='changed_perception_entries',
            field=models.ManyToManyField(related_name='changed_perc', to='entries.Entry'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]

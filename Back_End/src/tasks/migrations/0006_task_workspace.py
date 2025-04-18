# Generated by Django 5.1.7 on 2025-04-16 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_remove_category_option_task_category_and_more'),
        ('workspaces', '0003_alter_users_workspaces_user_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='workspace',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace'),
        ),
    ]

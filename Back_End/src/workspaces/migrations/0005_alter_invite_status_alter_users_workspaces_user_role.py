# Generated by Django 5.1.7 on 2025-04-19 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0004_alter_invite_status_alter_users_workspaces_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=8),
        ),
        migrations.AlterField(
            model_name='users_workspaces',
            name='user_role',
            field=models.CharField(choices=[('owner', 'Owner'), ('can_edit', 'Can Edit'), ('can_view', 'Can View')], default='can_view', max_length=8),
        ),
    ]

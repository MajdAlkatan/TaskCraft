# Generated by Django 5.1.7 on 2025-04-21 10:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_task_end_date_alter_task_start_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users_tasks',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_task', to='tasks.task'),
        ),
        migrations.AlterField(
            model_name='users_tasks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workspace_category_option',
            name='category_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.category_option'),
        ),
        migrations.AlterField(
            model_name='workspace_category_option',
            name='task_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='tasks.task_category'),
        ),
    ]

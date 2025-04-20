from django.db import migrations, models
import uuid

def generate_unique_uuids(apps, schema_editor):
    Workspace = apps.get_model('workspaces', 'Workspace')
    for obj in Workspace.objects.all():
        while True:
            new_uuid = uuid.uuid4()
            # Double-check this UUID doesn't exist (extremely unlikely but safe)
            if not Workspace.objects.filter(code=new_uuid).exists():
                obj.code = new_uuid
                obj.save(update_fields=['code'])
                break

class Migration(migrations.Migration):
    dependencies = [
        ('workspaces', '0008_add_workspace_code_field'),
    ]

    operations = [
        migrations.RunPython(generate_unique_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='Workspace',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]
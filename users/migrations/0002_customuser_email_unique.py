from django.db import migrations, models

def remove_duplicate_emails(apps, schema_editor):
    CustomUser = apps.get_model('users', 'CustomUser')
    seen_emails = set()
    for user in CustomUser.objects.all():
        if user.email in seen_emails:
            user.delete()
        else:
            seen_emails.add(user.email)

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate_emails),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(unique=True),
        ),
    ]
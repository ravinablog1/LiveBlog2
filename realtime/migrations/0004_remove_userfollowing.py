from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0003_remove_notification_related_object_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserFollowing',
        ),
    ]
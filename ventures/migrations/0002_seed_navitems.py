from django.db import migrations



def seed_nav_items(apps, schema_editor):
    NavItem = apps.get_model('ventures', 'NavItem')

    items = [
        {'label': 'Home', 'url_name': 'ventures:home', 'order': 1},
        {'label': 'About', 'url_name': 'ventures:about', 'order': 2},
    ]

    for item in items:
        NavItem.objects.get_or_create(
            url_name=item['url_name'],
            defaults={
                'label': item['label'],
                'order': item['order'],
                'is_active': True,
                'open_in_new_tab': False,
            },
        )



def unseed_nav_items(apps, schema_editor):
    NavItem = apps.get_model('ventures', 'NavItem')
    NavItem.objects.filter(url_name__in=['ventures:home', 'ventures:about']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('ventures', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_nav_items, unseed_nav_items),
    ]

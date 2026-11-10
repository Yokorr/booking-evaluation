from django.db import migrations

def seed(apps, schema_editor):
    Location = apps.get_model('rooms', 'Location')
    Room = apps.get_model('rooms', 'Room')
    data = {
        'lyo': ('Lyon', [('lyo-desk', 'Open desk', 4), ('lyo-room', 'Meeting room', 6)]),
        'par': ('Paris', [('par-desk', 'Focus desk', 2), ('par-room', 'Boardroom', 10)]),
        'nan': ('Nantes', [('nan-room', 'Workshop room', 8)]),
    }
    for location_code, (city, rooms) in data.items():
        loc = Location.objects.create(code=location_code, city=city)
        for code, name, capacity in rooms:
            Room.objects.create(location=loc, code=code, name=name, capacity=capacity)

def unseed(apps, schema_editor):
    Room = apps.get_model('rooms', 'Room')
    Location = apps.get_model('rooms', 'Location')
    Room.objects.filter(code__in=['lyo-desk','lyo-room','par-desk','par-room','nan-room']).delete()
    Location.objects.filter(code__in=['lyo','par','nan']).delete()

class Migration(migrations.Migration):
    dependencies = [('rooms', '0001_initial')]
    operations = [migrations.RunPython(seed, unseed)]

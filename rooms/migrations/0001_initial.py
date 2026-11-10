from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('code', models.SlugField(max_length=12, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SlugField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.PositiveIntegerField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rooms', to='rooms.location')),
            ],
        ),
    ]

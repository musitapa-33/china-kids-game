from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbr', models.CharField(max_length=10)),
                ('capital', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=20)),
                ('emoji', models.CharField(max_length=10)),
                ('features', models.JSONField()),
                ('fact', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProvinceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=200)),
                ('caption', models.CharField(max_length=200)),
                ('is_png', models.BooleanField(default=False)),
                ('province', models.ForeignKey(on_delete=models.CASCADE, related_name='images', to='provinces.province')),
            ],
        ),
    ]

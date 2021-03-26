# Generated by Django 3.1.7 on 2021-03-16 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(default=2021, help_text='Year in YYYY format, ie 2020', max_length=10)),
                ('type', models.CharField(choices=[('R', 'Regular Season'), ('P', 'Postseason'), ('Pre', 'Preseason')], default='R', max_length=20, null=True)),
            ],
        ),
    ]

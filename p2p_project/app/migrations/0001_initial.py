# Generated by Django 4.2.2 on 2023-11-05 17:37

from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [

        migrations.CreateModel(
            name='ExchangeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='TicketsTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('orders', models.CharField(max_length=7)),
                ('available', models.FloatField()),
                ('max_limit', models.FloatField()),
                ('min_limit', models.FloatField()),
                ('rate', models.CharField(max_length=8)),
                ('pay_methods', models.TextField()),
                ('currency', models.CharField(max_length=5)),
                ('coin', models.CharField(max_length=5)),
                ('trade_type', models.BooleanField()),
                ('link', models.URLField()),
                ('time_create', models.DateTimeField()),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.exchangetable')),
            ],
            options={
                'verbose_name_plural': 'Tickets table',
                'ordering': ['-price', '-time_create'],
            },
        ),
    ]

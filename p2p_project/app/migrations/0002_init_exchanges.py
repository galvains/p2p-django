from django.db import migrations


def insert_ex(apps, schema_editor):
    Exchanges = apps.get_model('app', 'ExchangeTable')
    Exchanges.objects.create(id=1, name='Binance')
    Exchanges.objects.create(id=2, name='Bybit')
    Exchanges.objects.create(id=3, name='Paxful')
    Exchanges.objects.create(id=4, name='OKX')


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_ex),
    ]

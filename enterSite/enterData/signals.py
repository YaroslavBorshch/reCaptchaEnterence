from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Account


@receiver(post_migrate)
def populate_data_on_migration(sender, **kwargs):
    if sender.name == 'enterData':
        isEmpty = Account.objects.first()
        if not isEmpty:
            Account.objects.create(username='wrong_pass_user', password='null', email='any@email.com')
            Account.objects.create(username='right_pass_us', password='rfHDSnm2kohg', email='8v30cc3cmc@rentforsale7.com')
            Account.objects.create(username='coolSiteTwice', password='broke', email='mgb82we3m4@greencafe24.com')



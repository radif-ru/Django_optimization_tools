from django.core.management.base import BaseCommand

from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    help = 'Create user profiles'

    def handle(self, *args, **options):
        # print(ShopUser.objects.filter(shopuserprofile__isnull=True).count())
        for user in ShopUser.objects.filter(shopuserprofile__isnull=True):
            user.shopuserprofile = ShopUserProfile.objects.create(user=user)
            user.save()

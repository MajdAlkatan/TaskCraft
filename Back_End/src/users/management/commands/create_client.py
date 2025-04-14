from django.core.management.base import BaseCommand , CommandError
from django.conf import settings

from users.models import Client

class Command(BaseCommand):
    help = "creating the client we need for api just in Debug, it will be unavailable in production"

    def handle(self, *args, **options):
        if settings.DEBUG:
            # get or create our client
            client = Client.objects.filter(username="Majd").first()
            if not client:
                client = Client.objects.create(
                    username = "Majd",
                    secret= """sl:a,"hd?1he:l3z4dxvx=f2342jr0io9)54(-)[4j2f+(d0j545323fs\*sdf/sks%dnv,`ls#dfkl}"""
                )
        else:
            raise CommandError("Website Is In Production !")
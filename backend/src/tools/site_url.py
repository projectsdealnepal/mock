from django.contrib.sites.models import Site
from django.conf import settings

def get_site_url():
    # Get the current Site object
    current_site = Site.objects.get_current()

    # Get the domain name and protocol
    domain = current_site.domain
    protocol = 'https' if settings.USE_HTTPS else 'http'

    # Get the full URL for the MyModel object
    domain_name = f"{protocol}://{domain}"

    return domain_name
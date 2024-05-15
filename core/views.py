from django.conf import settings
from django.shortcuts import render
from users.client import oAuth2Client


def landing_page(request):
    client = oAuth2Client(
        client_id = settings.CLIENT_ID,
        client_secret = settings.CLIENT_SECRET,
        redirect_uri = settings.REDIRECT_URI,
        authorize_url = settings.AUTHORIZE_URL,
        token_url = settings.ACCESS_TOKEN_URL,
        resource_owner_url = settings.RESOURCE_OWNER_URL
    )

    ctx = {
        'authorization_url': client.get_authorization_url()
    }
    return render(request, 'landing.html', ctx)

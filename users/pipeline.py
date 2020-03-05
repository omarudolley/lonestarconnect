from .models import Profile
from urllib.request import urlopen

from PIL import Image
from io import BytesIO



def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        profile = Profile.objects.get(user=user)
        print(profile.url)
        profile.url = url
        print(profile.url)
        profile.save()

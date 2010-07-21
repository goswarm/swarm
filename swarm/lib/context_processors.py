from django.conf import settings

def media(request):
	from django.conf import settings
	return {'MEDIA_URL': settings.MEDIA_URL}

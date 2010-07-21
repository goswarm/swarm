def return_json_response(context={}):
    from django.http import HttpResponse
    from swarm.utils import myjson as json
    return HttpResponse(json.dumps(context))

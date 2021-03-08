from django.shortcuts import render, HttpResponse, Http404

import json
# Create your views here.

def dismiss_marketing_message(request):
    if request.is_ajax():
        data = {"success":True}
        print(data)
        json_data = json.dumps(data)
        print(json_data)
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404
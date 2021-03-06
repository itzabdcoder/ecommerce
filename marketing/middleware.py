from .models import MarketingMessage

class DisplayMarketing(object):
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_request(self, request):
        try:
            request.session['marketing_message'] = MarketingMessage.objects.all()[0].message
        except:
            request.session['marketing_message'] = False
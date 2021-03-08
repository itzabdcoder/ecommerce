import datetime
from .models import MarketingMessage
from django.utils import timezone
class DisplayMarketing():
    print(timezone.now())
    print(timezone.now() + datetime.timedelta(hours=8))
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_request(self, request):
        print("hii")
        try:
            request.session['marketing_message'] = MarketingMessage.objects.get_featured_item().message
        except:
            request.session['marketing_message'] = False
import datetime
from .models import MarketingMessage
from django.utils import timezone

def is_offset_greater(time_string_offset):
    print("grate")
    time1 = str(timezone.now())[:19]
    offset_time = time_string_offset[:19]
    offset_time_formatted = datetime.datetime.strptime(offset_time, "%Y-%m-%d %H:%M:%S")
    offset_time_tz_aware = timezone.make_aware(offset_time_formatted, timezone.get_default_timezone())
    now_time_formatted = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    now_time_tz_aware = timezone.make_aware(now_time_formatted, timezone.get_default_timezone())
    print(timezone.now)   
    print(now_time_tz_aware)
    print(offset_time_tz_aware)
    print(now_time_tz_aware > offset_time_tz_aware)
    return now_time_tz_aware > offset_time_tz_aware


class DisplayMarketing(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_request(self, request):
        try:
            message_offset = request.session['dismiss_message_for']
            print(message_offset)
        except:
            message_offset = None
        
        try:
            marketing_message = MarketingMessage.objects.get_featured_item().message
        except:
            marketing_message = False
        if message_offset is None:
            request.session['marketing_message'] = marketing_message
        elif message_offset is not None and is_offset_greater(message_offset):
            request.session['marketing_message'] = marketing_message
        else:
            try:
                del request.session['marketing_message']
            except:
                pass
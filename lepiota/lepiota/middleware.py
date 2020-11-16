from lepiota.settings import FRONTEND_ADDRESS

def frontend_middleware(get_response):
    def middleware(request):

        response = get_response(request)
	    
        if 'HTTP_REFERER' in request.META:
            if request.META['HTTP_REFERER'].startswith(FRONTEND_ADDRESS):
                response["Access-Control-Allow-Origin"] = FRONTEND_ADDRESS
        
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "*"
        response['token'] = "*"
        response['expires_at'] = "*"

        return response
    return middleware

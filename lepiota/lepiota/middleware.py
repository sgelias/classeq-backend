from lepiota.settings import FRONTEND_ADDRESS

def frontend_middleware(get_response):
    def middleware(request):

        response = get_response(request)
        print(response)

        if 'HTTP_REFERER' in request.META:

            print("Meta: " + request.META['HTTP_REFERER'])
            print("Frontend: " + FRONTEND_ADDRESS)

            if request.META['HTTP_REFERER'].startswith(FRONTEND_ADDRESS):
                response["Access-Control-Allow-Origin"] = FRONTEND_ADDRESS

        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "*"
        response['token'] = "*"
        response['expires_at'] = "*"

        return response
    return middleware

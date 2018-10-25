class PutAndDeleteParsingMiddleware:
    """
    Allow to parse PUT and DELETE request without having to use a REST framework
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        
    def __call__(self, request):
        if request.method == 'PUT':
            if hasattr(request, '_post'):
                del request._post
                del request._files
            try:
                request.method = 'POST'
                request._load_post_and_files()
                request.method = 'PUT'
            except AttributeError as e:
                request.META['REQUEST_METHOD'] = 'POST'
                request._load_post_and_files()
                request.META['REQUEST_METHOD'] = 'PUT'

            request.PUT = request.POST
        elif request.method == 'DELETE':
            if hasattr(request, '_post'):
                del request._post
                del request._files
            try:
                request.method = 'POST'
                request._load_post_and_files()
                request.method = 'DELETE'
            except AttributeError as e:
                request.META['REQUEST_METHOD'] = 'POST'
                request._load_post_and_files()
                request.META['REQUEST_METHOD'] = 'DELETE'

            request.DELETE = request.POST
        
        return self.get_response(request)
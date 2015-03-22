class TrackingMiddleware:
    def process_request(self, request):
        print(dict(request.session))

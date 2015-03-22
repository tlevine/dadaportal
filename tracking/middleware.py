class TrackingMiddleware:
    def process_request(self, request):
        if 'session_id' not in request.session:
            request.session['session_id'] = random.getrandbits(128)

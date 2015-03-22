from .models import Hit

class TrackingMiddleware:
    def process_request(self, request, response):
        'Generate the hit identifier.'
        request.hit_id = rand()
    def process_response(self, request, response):
        'Get the status code.'
        Hit.objects.filter(hit = request.hit_id).update(status_code = response.status_code))
        return response

def big(request):
    return {'big': 'slides' in request.GET}

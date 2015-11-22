def plot(query):
    def view(request):
        return render(request, 'plot.html')
    return view

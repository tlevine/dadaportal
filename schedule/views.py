import subprocess

from django.shortcuts import render

def schedule(request):
    p = subprocess.Popen('pal -c 1 --html'.split(),
            stdout = subprocess.PIPE)
    p.wait()
    return render(request, 'schedule.html', {'schedule': p.stdout.read().decode('utf-8')})

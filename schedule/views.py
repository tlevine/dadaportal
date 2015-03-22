import subprocess

from django.shortcuts import render

def pal(command):
    p = subprocess.Popen(command.split(),
            stdout = subprocess.PIPE)
    p.wait()
    return p.stdout.read().decode('utf-8')

def day(request):
    html = '<pre>%s</pre>' % pal('pal --nocolor -r 2')
    return render(request, 'schedule.html', {'schedule': html})

def month(request):
    return render(request, 'schedule.html', {'schedule': pal('pal -c 1 --html')})


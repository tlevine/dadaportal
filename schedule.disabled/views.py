import subprocess

from django.shortcuts import render
from django.views.generic import TemplateView

def pal(command):
    p = subprocess.Popen(command.split(),
            stdout = subprocess.PIPE)
    p.wait()
    return p.stdout.read().decode('utf-8')

index = TemplateView.as_view(template_name = 'schedule.html')

def day(request):
    text = pal('pal --mail --nocolor -r 2').partition('\n\n')[2]
    html = '<pre>%s</pre>' % text
    return render(request, 'schedule.html', {'schedule': html})

def month(request):
    return render(request, 'schedule.html', {'schedule': pal('pal -c 1 --html')})

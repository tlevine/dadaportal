from django.views.generic import TemplateView
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render

index = TemplateView.as_view(template_name = 'index.html')

def docs(request):
    with open(os.path.join(settings.BASE_DIR, 'requirements.txt')) as fp:
        requirements = [line.strip() for line in fp]
    params = {
        'requirements': requirements,
        'database': DATABASES['default']
        'notmuch_dir': os.path.join(settings.NOTMUCH_DB, 'mail'),
    }
    base = get_template('install.md').render(Context(params))
    return render(request, 'base.html', {'base': base})

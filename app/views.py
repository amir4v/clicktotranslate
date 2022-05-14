from django.shortcuts import render
from django.http import HttpResponse
from .models import Word


def index(request):
    return render(request, 'index.html')


def translate(request):
    if request.method == 'GET':
        en = request.GET.get('word').lower()
        line = Word.objects.get(en=en).line
        return HttpResponse(line)

    text = list(request.POST['text'])
    for t in text:
        if t not in 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP1234567890 ':
            text.remove(t)
    text = ''.join(text)
    text = text.replace('\n\n', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('  ', ' ')
    text = text.split(' ')
    return render(request, 'translate.html', {'text': text})

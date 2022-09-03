from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Word, Text
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # from stuff import read_from_both as r
    # from app.models import Word
    # words = [
    #     Word(en=w[0], fa=w[1]) for w in r.get()
    # ]
    # Word.objects.bulk_create(words)

    texts = Text.objects.all()
    return render(request, 'index.html', {'texts': texts})


def new_text(request):
    title = request.POST['title']
    content = request.POST['content']
    Text.objects.create(title=title, content=content)
    return redirect('/')


@csrf_exempt
def translate(request, id=0, s=''):
    if request.method == "GET":
        text = Text.objects.get(pk=id)
        content = text.content.split(' ')
        text_id = text.id
        return render(request, 'translate.html', {'content': content, 'text_id': text_id})
    
    en = list(request.POST.get('word').lower())
    for c in en:
        if c not in 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP':
            en.remove(c)
    en = ''.join(en)
    
    word = Word.objects.get(en=en)
    return JsonResponse(
        {
            'id': word.id,
            'word':str(word)
            }
        )


@csrf_exempt
def i_do_not_know(request):
    word_id = request.POST['word_id']
    text_id = request.POST['text_id']
    text = Text.objects.get(pk=text_id)
    word = Word.objects.get(pk=word_id)
    if not text.words.exists(word):
        text.words.add(word)
    return HttpResponse("OK")


def i_do_not_know_list(request, id):
    text = Text.objects.get(pk=id)
    words = text.words.all()
    return render(request, 'i-do-not-know_list.html', {'words': words})

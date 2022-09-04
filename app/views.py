from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Word, Text
from django.views.decorators.csrf import csrf_exempt


def index(request):
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
        content = text.content.split()
        return render(request, 'translate.html', {'content': content, 'text': text})
    
    en = list(request.POST.get('word').lower())
    for c in en:
        if c not in 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP':
            en.remove(c)
    en = ''.join(en)
    
    word = Word.objects.get(en=en)
    return JsonResponse(
        {
            'id': word.id,
            'word': str(word)
            }
        )


@csrf_exempt
def i_do_not_know(request):
    word_id = request.POST['word_id']
    text_id = request.POST['text_id']
    text = Text.objects.get(pk=text_id)
    word = Word.objects.get(pk=word_id)
    if not text.words.filter(pk=word_id).exists():
        text.words.add(word)
    return HttpResponse("OK")


def i_do_not_know_list(request, id):
    text = Text.objects.get(pk=id)
    words = text.words.all()
    return render(request, 'i-do-not-know_list.html', {'words': words, 'text': text})


def word_delete(request, id, text_id):
    word = Word.objects.get(pk=id)
    text = Text.objects.get(pk=text_id)
    
    text.words.remove(word)
    return redirect(f'/i-do-not-know-list/{text_id}')


def text_delete(request, id):
    Text.objects.get(pk=id).delete()
    return redirect('/')

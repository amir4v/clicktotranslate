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
    
    # (Words of): title - Words
    title = title + ' - Words'
    content = '\n '.join((
        word
            for word in
                set(content.lower().split())
    ))
    Text.objects.create(title=title, content=content)
    
    return redirect('/')


@csrf_exempt
def translate(request, id=0, s=''):
    if request.method == "GET":
        text = Text.objects.get(pk=id)
        content = text.content
        
        if text.title.endswith(' - Words'):
            # [:START Show all words from last word that i checked that as i-do-not-know]
            try:
                last_word = text.words.order_by('app_text_words.id').last().en # last_word_that_i_do_not_know
                last_index = content.find(last_word) + len(last_word) # last_word_last_index
            except:
                last_index = 0
            content = content[last_index:]
            # [:END]
            br = True
            content = [w.strip() for w in content.replace('\n', ' ').replace('  ', ' ').split()]
        else:
            br = False
            content = [w.strip() for w in content.replace('\n', '<br>').replace('  ', ' ').split()]
        
        return render(request, 'translate.html', {'content': content, 'text': text, 'br': br})
    
    en = list(request.POST.get('word').lower().strip().replace('<br>', ''))
    en = [
        c for c in en if c in 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP'
    ]    
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


@csrf_exempt
def i_do_not_know_checkbox(request):
    operation = request.POST['operation']
    
    text_id = request.POST['text_id']
    text = Text.objects.get(pk=text_id)
    
    en = request.POST['word']
    en = list(en.lower().strip().replace('<br>', ''))
    en = [
        c for c in en if c in 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP'
    ]    
    en = ''.join(en)
    word = Word.objects.get(en=en)
    
    if operation == 'add':
        if not text.words.filter(pk=word.id).exists():
            text.words.add(word)
    
    if operation == 'remove':
        text.words.remove(word)
    
    return HttpResponse("OK")


def i_do_not_know_list(request, id):
    text = Text.objects.get(pk=id)
    words = text.words.order_by('app_text_words.id')
    
    return render(request, 'i-do-not-know_list.html', {'words': words, 'text': text})


def word_delete(request, id, text_id):
    word = Word.objects.get(pk=id)
    text = Text.objects.get(pk=text_id)
    
    text.words.remove(word)
    return redirect(f'/i-do-not-know-list/{text_id}')


def text_delete(request, id):
    Text.objects.get(pk=id).delete()
    return redirect('/')

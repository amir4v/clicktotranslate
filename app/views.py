from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Expression, Q, Subquery
from .models import Word, Text


def clean_en(en):
    en = list(en.lower().strip().replace('<br>', ''))
    en = [
        c for c in en if c in 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP'
    ]
    en = ''.join(en)
    return en


def index(request):
    texts = Text.objects.all()
    return render(request, 'index.html', {'texts': texts})


def new_text(request):
    title = request.POST['title']
    content = request.POST['content']
    text = Text.objects.create(title=title, content=content)
    
    words = tuple( clean_en(word) for word in set(content.lower().split()) )
    text.all_words.set(Word.objects.filter(en__in=words)) # All-Words that i have
    
    return redirect('/')


@csrf_exempt
def translate(request, id=0, all_words=False):
    if request.method == "GET":
        text = Text.objects.get(pk=id)
        
        if all_words:
            page=1
            pp = 100 # Per-Page
            
            words = text.all_words.filter \
                            (~Q(id__in=text.words_ik.values_list('id'))) \
                            .order_by('?') \
                            [
                                pp*(page-1)
                                :
                                pp*(page)
                            ]
            br = True
        else:
            words = text.all_words.all()
            br = False
        
        count = text.all_words.filter(
                                     ~Q(id__in=text.words_ik.values_list('id'))
                                     ).count()
        
        return render(request, 'translate.html', {'words': words, 'text': text, 'br': br, 'count':count})
    
    en = request.POST.get('word')
    en = clean_en(en)
    word = Word.objects.get(en=en)
    
    return JsonResponse(
        {
            'id': word.id,
            'word': str(word)
            }
        )


@csrf_exempt
def i_know_checkbox(request):
    operation = request.POST['operation']
    
    text_id = request.POST['text_id']
    text = Text.objects.get(pk=text_id)
    
    en = request.POST['word']
    en = clean_en(en)
    word = Word.objects.get(en=en)
    
    if operation == 'add':
        if not text.words_ik.filter(pk=word.id).exists():
            text.words_ik.add(word)
    
    if operation == 'remove':
        text.words_ik.remove(word)
    
    return HttpResponse("OK")


def word_delete(request, id, text_id):
    word = Word.objects.get(pk=id)
    text = Text.objects.get(pk=text_id)
    
    text.words_ik.remove(word)
    return redirect(f'/i-do-not-know-list/{text_id}')


def text_delete(request, id):
    Text.objects.get(pk=id).delete()
    return redirect('/')

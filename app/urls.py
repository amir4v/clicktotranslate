from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new-text', views.new_text),
    path('translate', views.translate), # POST
    path('translate/<int:id>', views.translate),
    path('translate/<int:id>/<int:all_words>', views.translate),
    path('word/delete/<int:id>/<int:text_id>', views.word_delete),
    path('text/delete/<int:id>', views.text_delete),
    path('i-know-checkbox', views.i_know_checkbox),
]

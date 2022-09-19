from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new-text', views.new_text),
    path('translate', views.translate),
    path('translate/<int:id>/<str:s>', views.translate),
    path('translate/<int:id>/<str:s>/<int:page>', views.translate),
    path('i-do-not-know', views.i_do_not_know),
    path('i-do-not-know-list/<int:id>', views.i_do_not_know_list),
    path('word/delete/<int:id>/<int:text_id>', views.word_delete),
    path('text/delete/<int:id>', views.text_delete),
    path('i-do-not-know-checkbox', views.i_do_not_know_checkbox),
]

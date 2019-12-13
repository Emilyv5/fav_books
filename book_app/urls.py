from django.urls import path
from . import views
import login_app

urlpatterns = [
    path('books', views.book),
    path('addbook', views.add_book),
    path('logout', views.logout),
    path('books/<num>', views.book_id),
    path('AddtoFavorite/<num>', views.add_to_favorite),
    path('delete/<num>', views.delete),
    path('unfavorite/<num>', views.unfavorite),
    path('edit/<num>', views.edit)
]

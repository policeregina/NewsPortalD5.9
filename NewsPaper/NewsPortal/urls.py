from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import NewsList, NewsDetail, NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete


urlpatterns = [
   path('', NewsList.as_view(), name = 'news_list'),
   path('news/create', NewsCreate.as_view(), name = 'news_create'),
   path('article/create', ArticleCreate.as_view(), name = 'article_create'),
   path('news/<int:pk>/edit', NewsUpdate.as_view(), name = 'news_update'),
   path('article/<int:pk>/edit', ArticleUpdate.as_view(), name = 'article_update'),
   path('news/<int:pk>/delete', NewsDelete.as_view(), name = 'news_delete'),
   path('article/<int:pk>/delete', ArticleDelete.as_view(), name = 'article_delete'),
   path('<int:pk>', NewsDetail.as_view(), name = 'news_detail'),
   path('search/', NewsList.as_view(template_name="news_search.html"), name = 'news_search')

]
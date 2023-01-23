from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post
from .filters import NewsFilter
from .forms import NewsForm



class NewsList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'newslist.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = 'sel_news'

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'PT'
        return super().form_valid(form)

class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'AR'
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'PT'
        return super().form_valid(form)
class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'
    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'AR'
        return super().form_valid(form)

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')

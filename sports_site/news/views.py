from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render#, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticleCreateForm

# Create your views here.
def home(request):
    league_slug = request.GET.get('league', None)
    Article_data = Article.objects.all().filter(league__url=league_slug).order_by('-id')[:10]
    context = {
        "articles": Article_data,
        }
    return render(request, 'news/home.html', context)


def news_detail(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        "article": article
        }
    return render(request, 'news/news_detail.html', context)


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'league.league_admin'
    template_name = 'news/new_article.html'
    model = Article
    form_class = ArticleCreateForm

    def get_success_url(self):
        url = f"/league/?league={self.request.GET.get('league')}"
        return url


class ArticleEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'league.league_admin'
    template_name = 'news/article_edit.html'
    model = Article
    form_class = ArticleCreateForm


    def get_success_url(self):
        url = f"/league/?league={self.request.GET.get('league')}"
        return url


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'league.league_admin'
    template_name = 'news/confirm_delete.html'
    model = Article

    def get_success_url(self):
        url = f"/league/?league={self.request.GET.get('league')}"
        return url


class ArticlesView(ListView):
    template_name = 'news/news_page.html'
    paginate_by=5
    model = Article
    context_object_name= 'articles'

    def get_queryset(self):
        league_slug = self.request.GET.get('league', None)
        queryset = Article.objects.all().filter(league__url=league_slug).order_by('-id')
        return queryset




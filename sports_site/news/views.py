from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticleCreateForm

# Create your views here.
def home(request):
    Article_data = Article.objects.all().order_by('-id')[:10]

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


#ToDo, change permissions to leagueadmin/ new creator
@login_required
@permission_required('league.league_admin')
def news_create(request):

    if request.method == 'POST':
        form = ArticleCreateForm(data=request.POST)
        if form.is_valid():
            new_article = form.save()
        return redirect('news-home')
    else:
        form = ArticleCreateForm()


    context = {
        "form": form
        }
    return render(request, 'news/new_article.html', context)

class ArticleCreateView(CreateView):
    template_name = 'news/new_article.html'
    model = Article
    form_class = ArticleCreateForm
    success_url = "/news"

class ArticleEditView(UpdateView):
    template_name = 'news/article_edit.html'
    model = Article
    form_class = ArticleCreateForm
    success_url = "/news"


class ArticleDeleteView(DeleteView):
    template_name = 'news/confirm_delete.html'
    model = Article
    success_url = "/news"


class ArticlesView(ListView):
    template_name = 'news/news_page.html'
    paginate_by=5
    model = Article
    context_object_name= 'articles'
    queryset = Article.objects.all().order_by('-id')




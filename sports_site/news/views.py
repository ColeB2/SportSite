from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView
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


def news_page(request):
    article_list = Article.objects.all().order_by('-id')
    paginator = Paginator(article_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
        }

    return render(request, 'news/news_page.html', context)


@login_required
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





class ArticlesView(ListView):
    template_name = 'news/news_page.html'
    paginate_by=5
    model = Article
    context_object_name= 'articles'
    queryset = Article.objects.all().order_by('-id')

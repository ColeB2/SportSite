from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView
from .models import Article

# Create your views here.
def home(request):
    Article_data = Article.objects.all().order_by('-id')[:10]

    context = {
        "articles": Article_data,
        }

    return render(request, 'news/home.html', context)

def news_detail(request, pk):
    article = Article.objects.get(pk=pk)
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


class ArticlesView(ListView):
    template_name = 'news/news_page.html'
    paginate_by=5
    model = Article
    context_object_name= 'articles'
    queryset = Article.objects.all().order_by('-id')

from django import forms
from django.forms import SelectDateWidget
from news.models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'date_posted', 'image',
            'image_description',
            ]


    def __init__(self, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
        self.fields['date_posted'].widget=SelectDateWidget()
        self.fields['image'].required=False
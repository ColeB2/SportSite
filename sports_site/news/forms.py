from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, MultiWidgetField
from django import forms
from django.forms import SelectDateWidget
from news.models import Article

from datetime import datetime

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'date_posted', 'image',
            'image_description']


    def __init__(self, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required=False

        cur_date = datetime.today()
        year_range = tuple([i for i in range(cur_date.year - 5, cur_date.year + 5)])
        self.fields['date_posted'] = forms.DateField(initial=cur_date, widget=SelectDateWidget(
            empty_label=("Year", "Month", "Day"), years=(year_range)
            ))
        self.fields['date_posted'].required = False

        #crispylayout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row("title", css_class="form-row"),
            Row("body", css_class="form-row"),
            Row("author", css_class="form-row"),
            Row(
                Column(
                    MultiWidgetField('date_posted', attrs=({'style': 'width: 33%; display: inline-block; '})),
                    css_class='form-group col-md-12'
                    ),
                css_class='form-row'
                ),
            Row("image", css_class="form-row"),
            Row("image_description", css_class="form-row"),
                )
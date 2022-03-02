from datetime import datetime, time
from django.test import TestCase
from news.forms import ArticleCreateForm



class ArticleCreateFormTest(TestCase):
    def test_article_form_labels(self):
        form = ArticleCreateForm()
        form_date_label = form.fields["date_posted"].label
        form_title_label = form.fields["title"].label
        form_body_label = form.fields["body"].label
        form_author_label = form.fields["author"].label
        form_image_label = form.fields["image"].label
        form_image_description_label = form.fields["image_description"].label

        self.assertTrue(form_date_label is None or form_date_label == "Date posted")
        self.assertTrue(form_title_label is None or form_title_label == "Title")
        self.assertTrue(form_body_label is None or form_body_label == "Body")
        self.assertTrue(form_author_label is None or form_author_label == "Author")
        self.assertTrue(form_image_label is None or form_image_label == "Image")
        self.assertTrue(form_image_description_label is None or form_image_description_label == "Image description")
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search$', views.search, name='search'),
    url(r'^my_products$', views.my_products, name='my_products'),
    url(r'^my_data', views.my_data, name='my_data'),
    url(r'^products/new$', views.products_new, name='products_new'),
    url(r'^products/edit/(?P<product_id>[\d]+)$', views.products_edit, name='products_edit'),
    url(r'^products/new/question/(?P<product_id>[\d]+)$', views.product_new_question, name='product_new_question'),
    url(r'^product/(?P<slug>[-\w\d]+)$', views.product_show, name='product_show'),
    url(r'^product/(?P<product_id>[\d]+)/questions/(?P<question_id>[\d]+)$', views.product_answer_question,
        name='product_answer_question'),
    url(r'^product/(?P<product_id>[\d]+)/questions$', views.product_question, name='product_question'),
]
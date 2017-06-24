from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from portal.forms import ProductForm, ProductQuestionForm, AnswerQuestionForm, UserForm, UserProfileForm
from portal.models import Product, Category, ProductQuestion, ProductAnswer, UserProfile
import algoliasearch_django as algoliasearch


def home(request):
    categories = Category.objects.filter(hidden=False, parent__isnull=True).exclude(categories__isnull=True).order_by(
        'name')
    context = {
        'categories': categories
    }
    return render(request, 'portal/home.html', context)


@login_required
def my_products(request):
    products = Product.objects.filter(user=request.user)
    context = {
        'products': products
    }
    return render(request, 'portal/my_products.html', context)


@login_required
def products_new(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = Product()
            product.user = request.user
            product.name = form.cleaned_data['name']
            product.quantity = form.cleaned_data['quantity']
            product.price = form.cleaned_data['price']
            product.shot_description = form.cleaned_data['shot_description']
            product.description = form.cleaned_data['description']
            product.status = 'Active'
            product.save()

            categories = Category.objects.filter(id__in=request.POST.getlist('categories'))
            if categories:
                for category in categories:
                    product.categories.add(category)

            return redirect('my_products')

    form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'portal/products_new.html', context)


@login_required
def products_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product.user != request.user:
        return HttpResponseForbidden

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.quantity = form.cleaned_data['quantity']
            product.price = form.cleaned_data['price']
            product.shot_description = form.cleaned_data['shot_description']
            product.description = form.cleaned_data['description']
            product.status = form.cleaned_data['status']
            product.categories = form.cleaned_data['categories']

            product.save()
            return redirect('my_products')

    form = ProductForm(instance=product)
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'portal/products_edit.html', context)


def product_show(request, slug):
    product = get_object_or_404(Product, slug=slug, status='Active')
    questions = ProductQuestion.objects.filter(product=product, status='Active')
    form = ProductQuestionForm()
    context = {
        'form': form,
        'product': product,
        'questions': questions
    }
    return render(request, 'portal/product_show.html', context)


@login_required
def product_new_question(request, product_id):
    product = get_object_or_404(Product, id=product_id, status='Active')

    if request.method == 'POST':
        form = ProductQuestionForm(request.POST)
        if form.is_valid():
            question = ProductQuestion()
            question.user = request.user
            question.product = product
            question.question = form.cleaned_data['question']
            question.status = 'Active'
            question.save()

    return redirect('product_show', product.slug)


@login_required
def product_question(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'portal/product_question.html', context)


@login_required
def product_answer_question(request, product_id, question_id):
    product = get_object_or_404(Product, pk=product_id)
    question = get_object_or_404(ProductQuestion, pk=question_id)

    form = AnswerQuestionForm()

    if request.method == 'POST':
        form = AnswerQuestionForm(request.POST)
        if form.is_valid():
            product_answer = ProductAnswer()
            product_answer.user = request.user
            product_answer.answer = form.cleaned_data['answer']
            product_answer.product_question = question
            product_answer.status = 'Active'
            product_answer.save()

            return redirect('product_question', product.id)

    context = {
        'form': form,
        'product': product,
        'question': question
    }

    return render(request, 'portal/product_answer_question.html', context)


def search(request):
    categories = Category.objects.filter(hidden=False, parent__isnull=True).order_by('name')
    qs = request.GET.get('qs', '')
    str_category = request.GET.get('category', '')
    page = request.GET.get('page', '0')

    results = None

    cat_name = ''
    next_page = ''
    previous_page = ''

    if page != 0:
        next_page = int(page) + 1
        previous_page = int(page) - 1

    if qs:
        params = {'hitsPerPage': 1, 'page': page}
        results = algoliasearch.raw_search(Product, qs, params)

    if str_category:
        cat = get_object_or_404(Category, slug=str_category)
        cat_name = cat.name
        results = Product.objects.filter(categories=cat)

        paginator = Paginator(results, 1)
        page = request.GET.get('page', 1)

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'results': results,
        'cat_name': cat_name,
        'str_category': str_category,
        'qs': qs,
        'next_page': next_page,
        'previous_page': previous_page
    }
    return render(request, 'portal/product_search.html', context)


@login_required
def my_data(request):
    user = User.objects.get(pk=request.user.pk)
    user_form = UserForm(instance=user)

    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()

    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()

            user_profile.cpf = profile_form.cleaned_data['cpf']
            user_profile.address = profile_form.cleaned_data['address']
            user_profile.address2 = profile_form.cleaned_data['address2']
            user_profile.number = profile_form.cleaned_data['number']
            user_profile.district = profile_form.cleaned_data['district']
            user_profile.city = profile_form.cleaned_data['city']
            user_profile.state = profile_form.cleaned_data['state']
            user_profile.country = profile_form.cleaned_data['country']
            user_profile.zipcode = profile_form.cleaned_data['zipcode']
            user_profile.phone = profile_form.cleaned_data['phone']
            user_profile.remote_receiver_id = profile_form.cleaned_data['remote_receiver_id']
            user_profile.save()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'portal/my_data.html', context)

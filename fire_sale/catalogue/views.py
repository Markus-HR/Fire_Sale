from django.shortcuts import render, redirect
from catalogue.models import Postings, Bids
from django.template.defaulttags import register
from django.http import JsonResponse
from static.python.CheckoutForms import CheckoutContact, CheckoutPayment, RatingForm


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    query = Postings.objects.filter(item__postings__open=True).order_by('-creation_date')
    context = {'data': get_post_item(query, request)}
    using_filter = False
    if 'search_filter' in request.GET:
        search_input = request.GET['search_filter']
        new_context = [x for x in context['data'] if x['name'] == search_input]
        context = None
        context = {'data': new_context}

    if using_filter:
        return JsonResponse(context)
    else:
        return render(request, 'catalogue/index.html', context)

#    sorted_post_items = sorted(post_items, key=lambda k: k['max_bid'], reverse=rev_order)


# open, date, itemid, name, item_pic, category, max_bid
# Create your views here.
def old_index(request):
    query = Postings.objects.filter(item__postings__open=True).order_by('-creation_date')
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(item__name__icontains=search_filter, item__postings__open=True)
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item})

    if 'sort_by' in request.GET:
        sort_filter = request.GET['sort_by']
        if sort_filter == 'name':
            sort_query = Postings.objects.filter(item__postings__open=True).order_by('item__name')
            post_item = get_post_item(sort_query, request)
        elif sort_filter == 'high_low':
            post_item = get_post_item_sort_price(True, request)
        elif sort_filter == 'low_high':
            post_item = get_post_item_sort_price(False, request)
        else:
            # Recent or unexpected sort by filters
            sort_query = Postings.objects.filter(item__postings__open=True).order_by('-creation_date')
            post_item = get_post_item(sort_query, request)
        return JsonResponse({'data': post_item})

    context = {'data': get_post_item(query, request)}
    return render(request, 'catalogue/index.html', context)


def get_post_item(query, request):
    post_item = [{
        'name': x.item.name,
        'item_pic': x.item.item_picture,
        'max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id)], default=0),
        'category': x.item.category.name,
        'date': x.creation_date,
        'open': x.open,
        'has_accepted_bid': check_accepted_bid(x.id)[0],
        'accepted_bid_amount': check_accepted_bid(x.id)[1][0],
        'itemid': x.item_id,
        'user_max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id, user_id=request.user.id)], default=0),
        'user_min_bid': min([y.price for y in Bids.objects.filter(posting_id=x.id, user_id=request.user.id)], default=0),
    } for x in query]
    return post_item


def check_accepted_bid(post_id):
    bids = Bids.objects.filter(posting_id=post_id, accept=True)
    if bids:
        return [True, [x.price for x in bids]]
    else:
        return [False, [0]]


def get_post_item_sort_price(rev_order, request):
    query = Postings.objects.filter(item__postings__open=True).order_by('-creation_date')
    post_items = get_post_item(query, request)
    sorted_post_items = sorted(post_items, key=lambda k: k['max_bid'], reverse=rev_order)
    return sorted_post_items


# My bids section
def my_bids(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(bids__user=request.user.id, item__name__icontains=search_filter, item__postings__open=True)
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item})
    query = Postings.objects.filter(bids__user=request.user.id, item__postings__open=True)
    context = {'data': get_post_item(query, request)}
    return render(request, 'catalogue/bids/my_bids.html', context)


def my_accepted_bids(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(bids__user=request.user.id, bids__accept=True, item__name__icontains=search_filter)
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item, 'accepted': 'accepted'})
    query = Postings.objects.filter(bids__user=request.user.id, bids__accept=True)
    context = {'data': get_post_item(query, request), 'accepted': 'accepted'}
    return render(request, 'catalogue/bids/my_bids.html', context)


# My postings section
def my_postings(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(user=request.user.id, item__name__icontains=search_filter)
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item})

    query = Postings.objects.filter(user=request.user.id)
    context = {'data': get_post_item(query, request)}
    return render(request, 'catalogue/posting/my_postings.html', context)


# Checkout section
def checkout(request):
    _remove_session_vars(request)
    if request.method == "POST":
        contact_form = CheckoutContact(data=request.POST)
        payment_form = CheckoutPayment(data=request.POST)
        rating_form = RatingForm(data=request.POST)

        if request.POST.get("Cancel") == "Cancel":
            return redirect("catalogue-index")
        if contact_form.is_valid():
            request.session['ContactForm'] = contact_form.get_data_dict()
            request.session['PaymentForm'] = payment_form.get_data_dict()
            request.session['RatingForm'] = rating_form.get_data_dict()
            return redirect('checkout_review')
    else:
        contact_form = CheckoutContact()
        payment_form = CheckoutPayment()
        rating_form = RatingForm()

    return render(request, 'catalogue/checkout/CheckoutAccordion.html', {
        'ContactForm': contact_form,
        'PaymentForm': payment_form,
        'RatingForm': rating_form,
    })


def session_checkout(request):
    if request.method == "POST":
        contact_form = CheckoutContact(data=request.POST)
        payment_form = CheckoutPayment(data=request.POST)
        rating_form = RatingForm(data=request.POST)
        _read_session_vars(request, contact_form, payment_form, rating_form)

        if request.POST.get("Cancel") == "Cancel":
            return redirect("catalogue-index")
        if contact_form.is_valid():
            request.session['ContactForm'] = contact_form.get_data_dict()
            request.session['PaymentForm'] = payment_form.get_data_dict()
            request.session['RatingForm'] = rating_form.get_data_dict()
            return redirect('checkout_review')
    else:
        contact_form = CheckoutContact()
        payment_form = CheckoutPayment()
        rating_form = RatingForm()
        _read_session_vars(request, contact_form, payment_form, rating_form)

    return render(request, 'catalogue/checkout/CheckoutAccordion.html', {
        'ContactForm': contact_form,
        'PaymentForm': payment_form,
        'RatingForm': rating_form,
    })


def checkout_review(request):
    if request.method == "POST":
        contact_form = CheckoutContact(data=request.POST)
        payment_form = CheckoutPayment(data=request.POST)
        rating_form = RatingForm(data=request.POST)
        _init_read_only_forms(request, contact_form, payment_form, rating_form)
        if request.POST.get("Back") == "Back":
            return redirect('session_checkout')
        if contact_form.is_valid() and rating_form.is_valid():
            return redirect('catalogue-index')
    else:
        contact_form = CheckoutContact()
        payment_form = CheckoutPayment()
        rating_form = RatingForm()
        _init_read_only_forms(request, contact_form, payment_form, rating_form)

    return render(request, 'catalogue/checkout/checkout_review.html', {
        'ContactForm': contact_form,
        'PaymentForm': payment_form,
        'RatingForm': rating_form,
    })


def _read_session_vars(request, contact_form, payment_form, rating_form):
    if 'ContactForm' in request.session:
        contact_form.read_from_dict(request.session['ContactForm'])
    if 'PaymentForm' in request.session:
        payment_form.read_from_dict(request.session['PaymentForm'])
    if 'RatingForm' in request.session:
        rating_form.read_from_dict(request.session['RatingForm'])


def _remove_session_vars(request):
    if 'ContactForm' in request.session:
        del request.session['ContactForm']
    if 'PaymentForm' in request.session:
        del request.session['PaymentForm']
    if 'RatingForm' in request.session:
        del request.session['RatingForm']


def _init_read_only_forms(request, contact_form, payment_form, rating_form):
    contact_form.read_from_dict(request.session['ContactForm'])
    payment_form.read_from_dict(request.session['PaymentForm'])
    rating_form.read_from_dict(request.session['RatingForm'])
    contact_form.disable_fields()
    payment_form.disable_fields()
    rating_form.disable_fields()
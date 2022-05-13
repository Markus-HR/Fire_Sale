from django.shortcuts import render, redirect
from catalogue.models import Postings, Bids
from django.template.defaulttags import register
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from checkout.models import Orders
from item.forms.Item_Information import ItemInfoForm
from item.forms.ShowItemPrice import ItemPriceForm
from static.python.CheckoutForms import *


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    query = Postings.objects.filter(item__postings__open=True).order_by('-creation_date')
    context = {'data': get_post_item(query, request)}
    using_filter = False
    if 'search_filter' in request.GET:
        search_input = request.GET['search_filter'].lower()
        data_list = context['data']
        new_data = [x for x in data_list if search_input in x['name'].lower()]
        # list(filter(lambda item: item['name'] == search_input, data_list))
        # next((i for i, x in enumerate(context['data']) if x['name'] == search_input), [])
        # [x for x in context['data'] if x['name'] == search_input]
        context = {'data': new_data}
        using_filter = True

    if 'sort_by' in request.GET:
        sort_input = request.GET['sort_by'].lower()
        data_list = context['data']
        if sort_input == 'name':
            new_data = sorted(data_list, key=lambda k: k['name'])
        elif sort_input == 'high_low':
            new_data = sorted(data_list, key=lambda k: k['max_bid'], reverse=True)
        elif sort_input == 'low_high':
            new_data = sorted(data_list, key=lambda k: k['max_bid'])
        else:
            new_data = sorted(data_list, key=lambda k: k['date'], reverse=True)
        context = {'data': new_data}
        using_filter = True

    if using_filter:
        return JsonResponse(context)
    else:
        return render(request, 'catalogue/index.html', context)


def get_post_item(query, request):
    post_item = [{
        'post_id': x.id,
        'name': x.item.name,
        'item_pic': x.item.image1,
        'max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id)], default=0),
        'category': x.item.category.name,
        'date': x.creation_date,
        'open': x.open,
        'has_accepted_bid': check_accepted_bid(x.id)[0],
        'accepted_bid_amount': check_accepted_bid(x.id)[1][0],
        'itemid': x.item_id,
        'user_max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id, user_id=request.user.id)],
                            default=0),
        'user_min_bid': min([y.price for y in Bids.objects.filter(posting_id=x.id, user_id=request.user.id)],
                            default=0),
    } for x in query]
    return post_item


def check_accepted_bid(post_id):
    bids = Bids.objects.filter(posting_id=post_id, accept=True)
    if bids:
        return [True, [x.price for x in bids]]
    else:
        return [False, [0]]


# My bids section
def my_bids(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(bids__user=request.user.id, item__name__icontains=search_filter,
                                               item__postings__open=True)
        post_item = get_post_item(search_query, request)
        return JsonResponse({'data': post_item})
    query = Postings.objects.filter(bids__user=request.user.id, item__postings__open=True)
    context = {'data': get_post_item(query, request)}
    return render(request, 'catalogue/bids/my_bids.html', context)


def my_accepted_bids(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        search_query = Postings.objects.filter(bids__user=request.user.id, bids__accept=True,
                                               item__name__icontains=search_filter)
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
def checkout(request, *args, **kwargs):
    _remove_session_vars(request)
    posting = get_object_or_404(Postings, id=kwargs['id'])
    item_form = _create_item_form(posting)
    bid_form = _create_max_bid_form(posting)

    if request.method == "POST":
        contact_form = ContactReviewForm(data=request.POST, prefix='contact')
        payment_form = PaymentReviewForm(data=request.POST, prefix='payment')
        rating_form = RatingForm(data=request.POST, prefix='rating')
        request.session['ContactForm'] = contact_form.get_data_dict()
        request.session['PaymentForm'] = payment_form.get_data_dict()
        request.session['RatingForm'] = rating_form.get_data_dict()
        return redirect('checkout_review', id=kwargs['id'])
    else:
        contact_form = ContactReviewForm(prefix='contact')
        contact_form.not_required_fields()
        payment_form = PaymentReviewForm(prefix='payment')
        payment_form.not_required_fields()
        rating_form = RatingForm(prefix='rating')

    return render(request, 'catalogue/checkout/CheckoutAccordion.html', {
        'ContactForm': contact_form,
        'PaymentForm': payment_form,
        'RatingForm': rating_form,
        'ItemForm': item_form,
        'BidForm': bid_form,
        'ItemImg': posting.item.image1
    })


def session_checkout(request, *args, **kwargs):
    posting = get_object_or_404(Postings, id=kwargs['id'])
    item_form = _create_item_form(posting)
    bid_form = _create_max_bid_form(posting)
    if request.method == "POST":
        contact_form = ContactReviewForm(data=request.POST, prefix='contact')
        payment_form = PaymentReviewForm(data=request.POST, prefix='payment')
        rating_form = RatingForm(data=request.POST, prefix='rating')
        request.session['ContactForm'] = contact_form.get_data_dict()
        request.session['PaymentForm'] = payment_form.get_data_dict()
        request.session['RatingForm'] = rating_form.get_data_dict()
        return redirect('checkout_review', id=kwargs['id'])
    else:
        contact_form = ContactReviewForm(
            instance=create_contact_model(request.session['ContactForm']),
            prefix='contact')
        contact_form.not_required_fields()
        payment_form = PaymentReviewForm(
            instance=create_payment_model(request.session['PaymentForm']),
            prefix='payment')
        payment_form.not_required_fields()
        rating_form = RatingForm(prefix='rating')
        rating_form.read_from_dict(request.session['RatingForm'])

    return render(request, 'catalogue/checkout/CheckoutAccordion.html', {
        'ContactForm': contact_form,
        'PaymentForm': payment_form,
        'RatingForm': rating_form,
        'ItemForm': item_form,
        'BidForm': bid_form,
        'ItemImg': posting.item.image1,
    })


def checkout_review(request, *args, **kwargs):
    posting = get_object_or_404(Postings, id=kwargs['id'])
    item_form = _create_item_form(posting)
    bid_form = _create_max_bid_form(posting)
    if request.method == "POST":
        contact_form = ContactReviewForm(data=request.POST, prefix='contact')
        payment_form = PaymentReviewForm(data=request.POST, prefix='payment')
        rating_form = RatingReviewForm(data=request.POST, prefix='rating')
        _init_read_only_forms(request, contact_form, payment_form, rating_form)
        if request.POST.get("Back") == "Back":
            return redirect('session_checkout', id=kwargs['id'])
        if contact_form.is_valid() and payment_form.is_valid():
            _commit_data(request,
                         posting,
                         contact_form,
                         payment_form)

            rating = request.session['RatingForm']['rating']
            if rating:
                _commit_rating(posting,
                               request.user,
                               rating)
            return redirect('catalogue-index')
    else:
        contact_form = ContactReviewForm(
            instance=create_contact_model(request.session['ContactForm']),
            prefix='contact')
        payment_form = PaymentReviewForm(
            instance=create_payment_model(request.session['PaymentForm']),
            prefix='payment')
        rating_form = RatingReviewForm(
            instance=create_rating_model(request.session['RatingForm']),
            prefix='rating')
        _init_read_only_forms(request, contact_form, payment_form, rating_form)

    return render(request, 'catalogue/checkout/checkout_review.html', {
        'ContactForm': contact_form,
        'PaymentForm': payment_form,
        'RatingForm': rating_form,
        'ItemForm': item_form,
        'BidForm': bid_form,
        'ItemImg': posting.item.image1,
    })


def _create_item_form(posting):
    item = posting.item
    item_form = ItemInfoForm(instance=item)
    item_form.disable_fields()
    return item_form


def _create_max_bid_form(posting):
    bid = Bids.objects.get(posting=posting, accept=True)
    bid_form = ItemPriceForm(instance=bid)
    bid_form.disable_fields()
    return bid_form


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
    contact_form.disable_fields()
    payment_form.disable_fields()
    rating_form.disable_fields()


def _commit_data(request, posting, contact_form, payment_form):
    contact = contact_form.save()
    payment = payment_form.save()

    order = Orders()
    order.posting = posting
    order.contact = contact
    order.payment = payment
    order.save()

    _close_posting(posting)


def _commit_rating(posting, user, rating):
    new_rating = Ratings()
    new_rating.posting = posting
    new_rating.user = user
    new_rating.rating = rating
    new_rating.save()


def _close_posting(posting):
    posting.open = False
    posting.save()

# from django.http import JsonResponse
# from django.shortcuts import render
#
# from reviews.forms import CreateReviewForm
# from reviews.models import Movie, Review
# from django.shortcuts import redirect
# from account.models import Account
#
# def movie_detail(request, slug):
#     context = {}
#     movie = Movie.objects.get(slug=slug)
#     reviews = movie.reviews.all()
#     account = request.user
#     form = CreateReviewForm(request.POST or None)
#     user_review_exists = False
#     user_review = None
#     if account.is_authenticated:
#         user_review_exists = reviews.filter(account_id=account, movie_id=movie.movie_id).exists()
#         print(user_review_exists)
#         if user_review_exists:
#             user_review = reviews.get(account_id=account, movie_id=movie.movie_id)
#             print(user_review.rating)
#             # form = CreateReviewForm(instance=user_review)
#     if form.is_valid():
#         rating = request.POST.get('rating')
#         review_text = request.POST.get('review_text')
#         review = Review.objects.create(
#             account_id=account,
#             movie_id=movie,
#             rating=rating,
#             review_text=review_text
#         )
#         context = {
#             'movie': movie,
#             'reviews': reviews,
#             "account": account,
#             'form': form,
#             'user_review_exists': user_review_exists,
#             'user_review': user_review,
#             'success': True
#         }
#         # return render(request, 'reviews/details.html', context)
#         return JsonResponse(context, status=200)
#     else:
#         form = CreateReviewForm()
#
#     context['form'] = form
#     context['movie'] = movie
#     context['reviews'] = reviews
#     context['account'] = account
#     context['user_review_exists'] = user_review_exists
#     context['user_review'] = user_review
#     context['success']: False
#     # return render(request, 'reviews/details.html', context)
#     return JsonResponse(context, status=400)
#
# # def create_review_view(request, slug):
# #     context = {}
# #     if not request.user.is_authenticated:
# #         return redirect('register')
# #     movie = Movie.objects.get(slug=slug)
# #     account = request.account
# #     form = CreateReviewForm(request.POST or None)
# #     if form.is_valid():
# #     #     obj = form.save(commit=False)
# #     #     author = Account.objects.get(user=request.user)
# #     #     obj.author = author
# #     #     obj.movie = movie
# #     #     obj.save()
# #     #     form = CreateReviewForm()
# #     # context['form'] = form
# #         rating = request.POST.get('rating')
# #         review_text = request.POST.get('review_text')
# #         review = Review.objects.create(
# #             account_id=account,
# #             movie_id=movie,
# #             rating=rating,
# #             review_text=review_text
# #         )
# #         return redirect('reviews:movie-detail', slug=slug)
# #     context = {
# #         'movie': movie
# #     }
# #     return render(request, 'reviews/details.html', context)
#
from decimal import InvalidOperation

from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from reviews.models import Movie, Review
from reviews.forms import CreateReviewForm, GlobalSearchForm
from account.models import Account


def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    reviews = movie.reviews.all()
    account = request.user if request.user.is_authenticated else None
    user_review = reviews.filter(account_id=account).first() if account else None
    form = CreateReviewForm()

    context = {
        'movie': movie,
        'reviews': reviews,
        'account': account,
        'user_review': user_review,
        'form': form,
    }
    return render(request, 'reviews/details.html', context)


@csrf_exempt
def create_review_ajax(request, slug):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, slug=slug)
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'User not authenticated.'}, status=403)

        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.account_id = request.user
            review.movie_id = movie
            review.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

from django.http import JsonResponse
from reviews.models import Review

def reviews_api(request, slug):
    if request.method == 'GET':
        reviews = Review.objects.filter(movie__slug=slug).values('rating', 'review_text', 'account_id__username')
        return JsonResponse({'reviews': list(reviews)}, safe=False)

def your_reviews_view(request):
    reviews = Review.objects.filter(account_id=request.user)
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/your_reviews.html', context)

def delete_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id, account_id=request.user)
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect('your_reviews')
    messages.error(request, "Invalid request method.")
    return redirect('your_reviews')



def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, account_id=request.user)

    if request.method == 'POST':
        form = CreateReviewForm(request.POST, instance=review)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Review updated successfully.")
                print("elo")
                return redirect('your_reviews')
            except InvalidOperation as e:
                messages.error(request, "Invalid input. Please check your values.")
    else:
        form = CreateReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})

def get_review_data(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return JsonResponse({
        'success': True,
        'review': {
            'rating': review.rating,
            'review_text': review.review_text,
        }
    })

def search_results_view(request):
    form = GlobalSearchForm(request.GET or None)
    results = []
    if form.is_valid() and form.cleaned_data['query']:
        query = form.cleaned_data['query']
        # Wyszukiwanie w polach: tytuł, rok i reżyser
        results = Movie.objects.filter(
            title__icontains=query
        ) | Movie.objects.filter(
            year__icontains=query
        ) | Movie.objects.filter(
            director__icontains=query
        )

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'search_results.html', context)
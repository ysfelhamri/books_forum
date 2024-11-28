from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, ReviewForm, RecommendationForm, DiscussionForm, ReplyForm, UserProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.contrib import messages
from .models import Review, Recommendation, Reply, Discussion, User
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.db.models import Count

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def add_edit_review(request, book_id, review_id=None):
    book = get_object_or_404(Book, id=book_id)
    
    if review_id:
        review = get_object_or_404(Review, id=review_id, book=book, user=request.user)
        if review.user != request.user:
            messages.error(request, "You can't edit this review.")
            return redirect('book-detail', pk=book.id)
    else:
        existing_review = Review.objects.filter(book=book, user=request.user).first()
        if existing_review:
            messages.error(request, 'You have already reviewed this book.')
            return redirect('book-detail', pk=book.id)
        review = None
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            if review:
                review.delete()
                messages.success(request, 'Your review has been deleted.')
            return redirect('book-detail', pk=book.id)
        else:
            form = ReviewForm(request.POST, instance=review, book=book)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                if review_id:
                    messages.success(request, 'Your review has been updated.')
                else:
                    messages.success(request, 'Your review has been added.')
                return redirect('book-detail', pk=book.id)
            else:
                messages.error(request, 'There was an error with your review.')
    else:
        form = ReviewForm(instance=review, book=book)
    
    return render(request, 'add-edit-review.html', {'form': form, 'book': book, 'review_id': review_id})

@login_required
def add_edit_recommendation(request, book_original_id, recommendation_id=None):
    book_original = get_object_or_404(Book, id=book_original_id)
    
    if recommendation_id:
        recommendation = get_object_or_404(Recommendation, id=recommendation_id, book_original=book_original, user=request.user)
        if recommendation.user != request.user:
            messages.error(request, "You can't edit this recommendation.")
            return redirect('book-detail', pk=book_original.id)
    else:
        recommendation = None
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            if recommendation:
                recommendation.delete()
                messages.success(request, 'Your recommendation has been deleted.')
            return redirect('book-detail', pk=book_original.id)
        else:
            form = RecommendationForm(request.POST, instance=recommendation, book_original=book_original)
            if form.is_valid():
                recommendation = form.save(commit=False)
                recommendation.book_original = book_original
                recommendation.user = request.user
                recommendation.save()
                if recommendation_id:
                    messages.success(request, 'Your recommendation has been updated.')
                else:
                    messages.success(request, 'Your recommendation has been added.')
                return redirect('book-detail', pk=book_original.id)
            else:
                messages.error(request, 'There was an error with your recommendation.')
    else:
        form = RecommendationForm(instance=recommendation, book_original=book_original)
    
    context = {
        'form': form,
        'book_original': book_original,
        'recommendation_id': recommendation_id,
    }
    
    return render(request, 'add-edit-recommendation.html', context)

@login_required
def add_discussion(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.book = book
            discussion.user = request.user
            discussion.save()
            Reply.objects.create(
                discussion=discussion,
                user=request.user,
                reply=form.cleaned_data['starting_topic'] 
            )
            messages.success(request, 'Your discussion has been added.')
            return redirect('book-detail', pk=book.id)
        else:
            messages.error(request, 'There was an error with your discussion.')
    else:
        form = DiscussionForm()
    
    return render(request, 'add-discussion.html', {'form': form, 'book': book})

class BookDiscussionDetail(DetailView):
    model = Discussion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discussion = self.get_object()
        replies = Reply.objects.filter(discussion=discussion)
        title = discussion.title

        # Initialize the form
        if self.request.user.is_authenticated:
            form = ReplyForm()
        else:
            form = None

        # Pagination
        paginator = Paginator(replies, 10)  # Show 10 replies per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'discussion': discussion,
            'replies': page_obj,
            'title': title,
            'form': form,
        }
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to add a reply.')
            return redirect('discussion-detail', pk=self.object.pk)

        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.discussion = self.object
            reply.user = request.user
            reply.save()
            messages.success(request, 'Your reply has been added.')
            return redirect('discussion-detail', pk=self.object.pk, book_id=self.object.book.id)
        else:
            messages.error(request, 'There was an error with your reply.')
            return self.get(request, *args, **kwargs)
        
@login_required
def edit_reply(request, reply_id, book_id, discussion_id):
    reply = get_object_or_404(Reply, id=reply_id)
    discussion = reply.discussion

    # Check if the reply is the first one in the discussion
    first_reply = Reply.objects.filter(discussion=discussion).order_by('created_date').first()

    if reply.user != request.user:
        messages.error(request, 'You cannot edit this reply.')
        return redirect('discussion-detail', pk=discussion.pk, book_id=discussion.book.id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            if reply == first_reply:
                messages.error(request, 'The first reply of the discussion cannot be deleted.')
            else:
                reply.delete()
                messages.success(request, 'Your reply has been deleted.')
            return redirect('discussion-detail', pk=discussion.pk, book_id=discussion.book.id)
        else:
            form = ReplyForm(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your reply has been updated.')
                return redirect('discussion-detail', pk=discussion.pk, book_id=discussion.book.id)
            else:
                messages.error(request, 'There was an error with your reply.')
    else:
        form = ReplyForm(instance=reply)
    
    context = {
        'form': form,
        'discussion': discussion,
        'reply_id': reply_id,
        'is_first_reply': reply == first_reply,
    }
    
    return render(request, 'edit-reply.html', context)

class UserProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['title'] = user_profile.username+"'s Profile"
        context['reviews'] = user_profile.reviews.all()
        context['recommendations'] = user_profile.recommendations.all()
        context['ratings'] = user_profile.ratings.all()
        context['discussions'] = user_profile.discussions.all()
        context['replies'] = user_profile.replies.all()
        return context
    


@login_required
def edit_profile(request, pk=None):
    user = request.user
    
    # Ensure that the user is trying to edit their own profile
    if pk and pk != user.pk:
        messages.error(request, 'You are not authorized to edit this profile.')
        return redirect('user-profile', pk=user.pk)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('user-profile', pk=user.pk)
        else:
            messages.error(request, 'There was an error updating your profile.')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'edit_profile.html', {'form': form})

def recent_recommendations(request):
    # Get the 10 most recent recommendations
    title = 'Recent Recommendations'
    recommendations = Recommendation.objects.filter(created_date__lte=now()).order_by('-created_date')[:10]
    return render(request, 'recent_recommendations.html', {'recommendations': recommendations, 'title': title})

def recent_reviews(request):
    # Get the 10 most recent reviews
    title = 'Recent Reviews'
    reviews = Review.objects.filter(created_date__lte=now()).order_by('-created_date')[:10]
    return render(request, 'recent_reviews.html', {'reviews': reviews, 'title': title})

def recent_discussions(request):
    # Get the 10 most recent discussions
    title = 'Recent Discussions'
    discussions = Discussion.objects.filter(created_date__lte=now()).order_by('-created_date').annotate(reply_count=Count('discussion_reply'))[:10]
    return render(request, 'recent_discussions.html', {'discussions': discussions, 'title': title})

def user_reviews(request, user_id):
    user = get_object_or_404(User, id=user_id)
    reviews_list = Review.objects.filter(user=user).order_by('-created_date')
    paginator = Paginator(reviews_list, 10)  # Show 10 reviews per page
    title = user.username + "'s Reviews"

    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    reviews.count = reviews_list.count()
    return render(request, 'user_reviews.html', {'user_profile': user, 'reviews': reviews, 'title': title})

def user_recommendations(request, user_id):
    user = get_object_or_404(User, id=user_id)
    recommendations_list = Recommendation.objects.filter(user=user).order_by('-created_date')
    paginator = Paginator(recommendations_list, 10)  # Show 10 recommendations per page
    title = user.username + "'s Recommendations"

    page_number = request.GET.get('page')
    recommendations = paginator.get_page(page_number)
    recommendations.count = recommendations_list.count()

    return render(request, 'user_recommendations.html', {'user_profile': user, 'recommendations': recommendations, 'title': title})

def user_discussions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    discussions_list = Discussion.objects.filter(user=user).order_by('-created_date').annotate(reply_count=Count('discussion_reply'))
    paginator = Paginator(discussions_list, 10)  # Show 10 discussions per page
    title = user.username + "'s Discussions"

    page_number = request.GET.get('page')
    discussions = paginator.get_page(page_number)
    discussions.count = discussions_list.count()

    return render(request, 'user_discussions.html', {'user_profile': user, 'discussions': discussions, 'title': title})
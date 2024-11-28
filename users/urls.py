from django.urls import path
from .views import signup_view, add_edit_review, add_edit_recommendation, add_discussion, BookDiscussionDetail, edit_reply, UserProfileView, edit_profile, recent_discussions,recent_reviews,recent_recommendations, user_reviews, user_recommendations, user_discussions


urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<int:pk>/edit/', edit_profile, name='edit-profile'),
    path('profile/<int:user_id>/reviews/', user_reviews, name='user-reviews'),
    path('profile/<int:user_id>/recommendations/', user_recommendations, name='user-recommendations'),
    path('profile/<int:user_id>/discussions/', user_discussions, name='user-discussions'),
    path("book/<int:book_id>/review/", add_edit_review, name="add-review"),
    path('recommendations/', recent_recommendations, name='recent-recommendations'),
    path('reviews/', recent_reviews, name='recent-reviews'),
    path('discussions/', recent_discussions, name='recent-discussions'),
    path("book/<int:book_id>/<int:review_id>/review/", add_edit_review, name="edit-review"),
    path("book/<int:book_original_id>/recommendation/", add_edit_recommendation, name="add-recommendation"),
    path("book/<int:book_original_id>/<int:recommendation_id>/recommendation/", add_edit_recommendation, name="edit-recommendation"),
    path("book/<int:book_id>/discussion/<int:pk>/", BookDiscussionDetail.as_view(template_name='discussion_detail.html'), name="discussion-detail"),
    path("book/<int:book_id>/discussion/", add_discussion, name="add-discussion"),
    path("book/<int:book_id>/discussion/<int:discussion_id>/edit-reply/<int:reply_id>/", edit_reply, name="edit-reply"),
]
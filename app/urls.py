from django.urls import path

from app.views.quotes import IndexView, TopQuotesView, AddQuoteView, LikeQuoteView, DislikeQuoteView, EditQuoteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('top/', TopQuotesView.as_view(), name='top_quotes'),
    path('add/', AddQuoteView.as_view(), name='add_quote'),
    path('like/<int:quote_id>/', LikeQuoteView.as_view(), name='like_quote'),
    path('dislike/<int:quote_id>/', DislikeQuoteView.as_view(), name='dislike_quote'),
    path('quote/edit/<int:pk>/', EditQuoteView.as_view(), name='edit_quote')
]

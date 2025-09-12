from django.urls import path
from django.contrib.auth import views as auth_views

from app.views.auth import RegisterView
from app.views.profile import ProfileView
from app.views.quotes import IndexView, AddQuoteView, LikeQuoteView, DislikeQuoteView, EditQuoteView
from app.views.top_quotes import TopQuotesView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('top/', TopQuotesView.as_view(), name='top_quotes'),
    path('add/', AddQuoteView.as_view(), name='add_quote'),
    path('like/<int:quote_id>/', LikeQuoteView.as_view(), name='like_quote'),
    path('dislike/<int:quote_id>/', DislikeQuoteView.as_view(), name='dislike_quote'),
    path('quote/edit/<int:pk>/', EditQuoteView.as_view(), name='edit_quote'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout')
]

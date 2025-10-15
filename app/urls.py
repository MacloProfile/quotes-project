from django.urls import path
from django.contrib.auth import views as auth_views

from app.views.actions_with_quotes.add_quote import AddQuoteView
from app.views.actions_with_quotes.delete_quote import DeleteQuoteView
from app.views.actions_with_quotes.edit_quote import EditQuoteView
from app.views.actions_with_quotes.vote_quote import VoteQuoteView
from app.views.auth import RegisterView
from app.views.profile.edit_user_info import ProfileSettingsView
from app.views.profile.profile import ProfileView
from app.views.quote_detail_view import QuoteAddedView
from app.views.quotes import IndexView

from app.views.top_quotes import TopQuotesView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('top/', TopQuotesView.as_view(), name='top_quotes'),
    path('add/', AddQuoteView.as_view(), name='add_quote'),
    path('quote/<int:pk>/added/', QuoteAddedView.as_view(), name='quote_added'),

    path('delete/<int:pk>/', DeleteQuoteView.as_view(), name='delete_quote'),

    path('vote/<int:quote_id>/<str:vote_type>/', VoteQuoteView.as_view(), name='vote_quote'),
    path('quote/edit/<int:pk>/', EditQuoteView.as_view(), name='edit_quote'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile_settings'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset/reset_form.html',
             email_template_name='password_reset/reset_email.html',
             success_url='/password_reset/done/'
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset/reset_confirm.html',
             success_url='/reset/done/'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/reset_complete.html'
         ),
         name='password_reset_complete')
]

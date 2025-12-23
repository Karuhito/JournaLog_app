from django.urls import path, include
from .views import SignupView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import JapaneseAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    # signup
    path('signup/', SignupView.as_view(), name='signup'),
    # login/logout
    path('login/', LoginView.as_view(authentication_form=JapaneseAuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

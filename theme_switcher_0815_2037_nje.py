# 代码生成时间: 2025-08-15 20:37:20
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator


# A model to store user settings
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, default=settings.DEFAULT_THEME)
    
    def __str__(self):
        return f"{self.user.username}'s theme settings"


# View to switch themes
class ThemeSwitcherView(View):
    def get(self, request, *args, **kwargs):
        # Handle GET request to display current theme settings
        user_settings = get_object_or_404(UserSettings, user=request.user)
        return render(request, 'theme_switcher/current_theme.html', {'theme': user_settings.theme})

    def post(self, request, *args, **kwargs):
        # Handle POST request to switch themes
        user_settings = get_object_or_404(UserSettings, user=request.user)
        new_theme = request.POST.get("theme")
        if new_theme in [t[0] for t in settings.THEME_CHOICES]:
            user_settings.theme = new_theme
            user_settings.save()
            return HttpResponseRedirect(reverse('theme_switcher'))
        else:
            # Handle error when theme is not valid
            return render(request, 'theme_switcher/error.html', {'error': 'Invalid theme selected'})


def theme_switcher(request):
    # Function-based view
    if request.method == 'POST':
        new_theme = request.POST.get('theme')
        user_settings = get_object_or_404(UserSettings, user=request.user)
        if new_theme in [t[0] for t in settings.THEME_CHOICES]:
            user_settings.theme = new_theme
            user_settings.save()
            return HttpResponseRedirect(reverse('theme_switcher'))
        else:
            return render(request, 'theme_switcher/error.html', {'error': 'Invalid theme selected'})
    else:
        user_settings = get_object_or_404(UserSettings, user=request.user)
        return render(request, 'theme_switcher/current_theme.html', {'theme': user_settings.theme})


# URL configuration
urlpatterns = [
    path('theme/', login_required(ThemeSwitcherView.as_view()), name='theme_switcher'),
]


# Example of settings.py
# Add new setting for theme choices
DEFAULT_THEME = 'light'
THEME_CHOICES = (
    ('light', 'Light'),
    ('dark', 'Dark'),
    ('blue', 'Blue'),
)

# Define the context processor to inject the current theme into the context
def theme_context_processor(request):
    if request.user.is_authenticated:
        return {'current_theme': UserSettings.objects.get(user=request.user).theme}
    return {}

TEMPLATES[0]['OPTIONS']['context_processors'].append('myapp.context_processors.theme_context_processor')

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.views.generic import TemplateView, RedirectView


urlpatterns = [

    # Administration
    path('admin/', admin.site.urls),
    
    # Accounts
    path('account/', include('account.urls', namespace='account')),

    # Oauth2
    path('api/v1/o/', include('oauth.urls', namespace='oauth2_provider')),

    # General purpose
    path('welcome/', TemplateView.as_view(template_name="welcome.html")),
    path('', RedirectView.as_view(url="/welcome/")),
    re_path(r'^$', RedirectView.as_view(url="/welcome/")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

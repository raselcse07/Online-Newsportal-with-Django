from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.contrib import admin


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^',include("Post.urls")),
    url(r'^gallery/',include("Gallery.urls")),
    url(r'^reporter/',include("Reporter.urls")),
    url(r'^instant_articles/',include("Instant_Article.urls")),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^', include("Homepage.urls"))

]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

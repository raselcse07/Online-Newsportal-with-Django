from django.conf.urls import url
from . import views

app_name="Post"

urlpatterns = [
    url(r'^category/new_category/$',views.CategoryCreate,name="category_create"),
    url(r'^post/new_post/$',views.PostCreateView,name="add_new_post"),
    url(r'^post/post_list/$',views.PostList,name="post_list"),
    url(r'^(?P<slug>[^/]+)/$',views.PostDetail,name="post_detail"),
    url(r'^category/(?P<category_slug>[^/]+)/$',views.CategoryDetail,name="category_detail"),
    url(r'^(?P<slug>[^/]+)/edit/$',views.PostUpdate,name="post_update"),
    url(r'^(?P<slug>[^/]+)/delete/$',views.PostDetele,name="post_delete"),
    url(r'^about/detail/$',views.about_views,name="about_page"),
    url(r'^contact/detail/$',views.contact_views,name="contact_page"),
    url(r'^privacy-policy/detail/$',views.privacy_views,name="privacy_page"),
    url(r'^advertisements/detail/$',views.advertisements_views,name="ads_page"),


    url('ajax/load-disticts/', views.load_disticts, name='ajax_load_disticts'),  # <-- this one here

]

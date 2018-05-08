from django.conf.urls import url
from . import views

app_name="Reporter"

urlpatterns = [
	url(r'^enter/$', views.UserLogin,name="user_login"),
	url(r'^logout/$', views.UserLogout,name="user_logout"),
    url(r'^add_new/$', views.Register,name="user_register"),
    url(r'^all_reporters/$', views.AllUsers,name="reporters"),
    url(r'^general_settings/create/$', views.GeneralSettingsCreate,name="general_settings_create"),
    url(r'^general_settings/update/$', views.GeneralSettingsUpdate,name="general_settings_update"),
    url(r'^theme_settings/enable/$', views.ThemeSettingsEnable,name="enable_settings"),
    url(r'^theme_settings/middle_widget/$', views.HomepageMiddleSectionWidget,name="middle_widget"),
    url(r'^theme_settings/middle_widget_below/$', views.HomepageMiddleSectionWidgetBelow,name="middle_widget_below"),
    url(r'^theme_settings/middle_widget_below_two/$', views.HomepageMiddleSectionWidgetBelowTwo,name="middle_widget_below_two"),
    url(r'^theme_settings/insert_header_footer/$', views.InsertHeaderFooterView,name="insert_header"),
    url(r'^footer/above/$', views.FooterAboveSectionView,name="footer_above"),
    url(r'^insatnt_article/$', views.Instant_Articles_Views,name="insatnt_article"),
    url(r'^seo/$', views.SEO_Views,name="seo_settings"),
    url(r'^(?P<user>[A-Za-z0-9].*)/dashboard/$', views.Dashboard,name="user_dashboard"),
    url(r'^(?P<user>[A-Za-z0-9].*)/dashboard/profile/detail/$', views.UserDetail,name="user_detail"),
    url(r'^(?P<user>[A-Za-z0-9].*)/dashboard/profile/edit/$', views.UserUpdate,name="user_update"),
    url(r'^ads/home_section/$', views.HomepageAdsSection,name="homepage_ads"),
	url(r'^ads/post_detail_ads/$', views.PostDetailAdsSection,name="post_detail_ads"),
	url(r'^ads/post_detail_ads/$', views.PostDetailAdsSection,name="post_detail_ads"),
	url(r'^general_settings/copyright/$', views.CopyRight_Section,name="copyright_section"),


]

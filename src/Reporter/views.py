from django.contrib.auth import (
								login,
								get_user_model,
								logout
								)
from django.utils.timezone import datetime
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import (
								render,
								HttpResponseRedirect,
								get_object_or_404
							)
from .forms import (
					UserCreationForm,
					UserLoginForm,
					UserUpdateForm,
					HomepageMiddleWidgetForm,
					InsertHeaderFooterForm,
					HomepageMiddleWidgetFormBelow,
					HomepageMiddleWidgetFormBelowTwo,
					FooterAboveSectionForm,
					GeneralSettingsForm,
					HomepageAdsForm,
					PostDetailAdsForm,
					CopyRightSectionForm,
					InstantArticleModelForm,
					SEOForm
					)

from .models import Profile
from Post.models import PostModel
from Homepage.models import (
							HomepageMiddleSection,
							InsertHeaderFooter,
							HomepageMiddleSectionBelow,
							HomepageMiddleSectionBelowTwo,
							FooterAboveSection,
							GeneralSettings,
							HomepageAds,
							PostDetailPageAds,
							CopyRightSection,
							SEO
							)
from Instant_Article.models import InstantArticleModel



User = get_user_model()





def Register(request,*args,**kwargs):

	form = UserCreationForm(request.POST or None)

	if form.is_valid():

		instance=form.save(commit=False)
		instance.save()
		messages.success(request, "User Created", extra_tags='html_safe')

	template_name="Reporter/register.html"
	context={

				"form":form

			}


	return render(request,template_name,context)


def UserLogin(request,*args,**kwargs):

	if not request.user.is_authenticated():

		form=UserLoginForm(request.POST or None)

		if form.is_valid():

				username_=form.cleaned_data.get("username")
				user_obj=User.objects.get(username__iexact=username_)
				login(request,user_obj)
				return HttpResponseRedirect(user_obj.get_absolute_url)


		template_name="Reporter/login.html"
		context={

				"form":form
				}

		return render(request,template_name,context)
	else:
		username_ = request.user.username
		user_obj = User.objects.get(username__iexact=username_)
		return HttpResponseRedirect(user_obj.get_absolute_url)


def UserLogout(request):

	logout(request)
	return HttpResponseRedirect("/reporter/enter")



def Dashboard(request,user=None):

	# try:

		total_posts 			= PostModel.objects.all() # All Posts
		user_post 				= PostModel.objects.filter(user=request.user) # Users All Post
		user_count 				= User.objects.all() # All Posts
		todays_post 			= PostModel.objects.filter(publish_date__day=datetime.today().day).count() # Todays total posts
		yesterday_post 			= PostModel.objects.filter(publish_date__day=datetime.today().day - 1).count() # Yesterdays total post
		this_month 				= PostModel.objects.filter(publish_date__month=datetime.today().month).count() # Total posts of this month
		todays_user_post 		= PostModel.objects.filter(user=request.user,publish_date__day=datetime.today().day).count() # Todays posts of users
		yesterday_user_post 	= PostModel.objects.filter(user=request.user,publish_date__day=datetime.today().day - 1).count() # Yesterdays posts of users
		this_month_user_post 	= PostModel.objects.filter(user=request.user,publish_date__month=datetime.today().month).count() # Total posts of users of this month

		# Check total users
		# for i in total_posts:
		# 	print(i.user)

		# Total Users

		user_list = []
		for i in User.objects.all():
			user_list.append(i)


		user1 					= PostModel.objects.filter(user=user_list[0]).count()
		user2 					= PostModel.objects.filter(user=user_list[1]).count()
		user3 					= PostModel.objects.filter(user=user_list[2]).count()


		template_name = "Reporter/dashboard.html"
		context={
			"total_posts":total_posts,
			"user_post":user_post,
			"user_count":user_count,
			"todays_post":todays_post,
			"yesterday_post":yesterday_post,
			"this_month":this_month,
			"todays_user_post":todays_user_post,
			"yesterday_user_post":yesterday_user_post,
			"this_month_user_post":this_month_user_post,
			"user1":user1,
			"user2":user2,
			"user3":user3,

		}

		return render(request,template_name,context)

	# except:

	# 	messages.info(request, "Add atleast 5 posts to view dashboard section.", extra_tags='html_safe')
	# 	return HttpResponseRedirect(reverse('Post:add_new_post'))


def AllUsers(request):

	qs = Profile.objects.all()

	template_name = "Reporter/all_users.html"
	context = {
			"qs":qs
	}

	return render(request,template_name,context)

def UserDetail(request,user=None):

	qs =get_object_or_404(Profile,username=request.user)
	template_name = "Reporter/user_detail.html"
	context = {
			"qs":qs
	}

	return render(request,template_name,context)

def UserUpdate(request,user=None):

	qs =get_object_or_404(Profile,username=request.user)
	form = UserUpdateForm(request.POST or None, request.FILES or None,instance=qs)

	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Updated", extra_tags='html_safe')

	template_name = "Reporter/user_update.html"
	context = {
			"form":form
	}

	return render(request,template_name,context)



def ThemeSettingsEnable(request):

	qs = HomepageMiddleSection.objects.all().count()

	if request.method == "POST" and "enable" in request.POST:

		HomepageMiddleSection.objects.create()
		InsertHeaderFooter.objects.create()
		HomepageMiddleSectionBelow.objects.create()
		HomepageMiddleSectionBelowTwo.objects.create()
		FooterAboveSection.objects.create()
		HomepageAds.objects.create()
		PostDetailPageAds.objects.create()
		CopyRightSection.objects.create()
		InstantArticleModel.objects.create()
		SEO.objects.create()
		messages.success(request,"Successfully Enabled", extra_tags='html_safe')
		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


	template_name = "Reporter/theme_settings_enable.html"
	context = {

				"qs":qs

			}

	return render(request,template_name,context)



def HomepageMiddleSectionWidget(request):

	try:
		qs = HomepageMiddleSection.objects.all()[0]
		form = HomepageMiddleWidgetForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/middle_widget.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


def InsertHeaderFooterView(request):

	try:
		qs = InsertHeaderFooter.objects.all()[0]
		form = InsertHeaderFooterForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/insert_header_footer.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))



def HomepageMiddleSectionWidgetBelow(request):

	try:
		qs = HomepageMiddleSectionBelow.objects.all()[0]
		form = HomepageMiddleWidgetFormBelow(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/middle_widget_below.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))



def HomepageMiddleSectionWidgetBelowTwo(request):

	try:
		qs = HomepageMiddleSectionBelowTwo.objects.all()[0]
		form = HomepageMiddleWidgetFormBelowTwo(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/middle_widget_below_two.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


def FooterAboveSectionView(request):

	try:
		qs = FooterAboveSection.objects.all()[0]
		form = FooterAboveSectionForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/footer_above.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


def GeneralSettingsCreate(request):

	form = GeneralSettingsForm(request.POST or None,request.FILES or None)
	qs = GeneralSettings.objects.all().count()

	if qs == 1:
		return HttpResponseRedirect(reverse('Reporter:general_settings_update'))

	elif qs == 0:
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request,"Successfully Saved", extra_tags='html_safe')
			return HttpResponseRedirect(reverse('Reporter:general_settings_update'))

	template_name = "Reporter/general_settings_create.html"
	context = {

		"form":form
	}

	return render(request,template_name,context)

def GeneralSettingsUpdate(request):

	try:

		qs = GeneralSettings.objects.all()[0]
		form = GeneralSettingsForm(request.POST or None,request.FILES or None,instance=qs)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request,"Successfully Saved", extra_tags='html_safe')


		template_name = "Reporter/general_settings_update.html"
		context = {

			"form":form,
			"qs":qs
		}

		return render(request,template_name,context)
	except:
		return HttpResponseRedirect(reverse('Reporter:general_settings_create'))


def HomepageAdsSection(request):

	try:
		qs = HomepageAds.objects.all()[0]
		form = HomepageAdsForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/homepage_ads.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


def PostDetailAdsSection(request):

	try:
		qs = PostDetailPageAds.objects.all()[0]
		form = PostDetailAdsForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/post_detail_ads.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


def CopyRight_Section(request):

	try:
		qs = CopyRightSection.objects.all()[0]
		form = CopyRightSectionForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/copyright_section.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


def Instant_Articles_Views(request):

	try:
		qs = InstantArticleModel.objects.all()[0]
		form = InstantArticleModelForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/instant_articles.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))


def SEO_Views(request):

	try:
		qs = SEO.objects.all()[0]
		form = SEOForm(request.POST or None,instance=qs)

		if qs:

			if form.is_valid():

				instance = form.save(commit=False)
				instance.save()
				messages.success(request,"Successfully Saved", extra_tags='html_safe')

		template_name = "Reporter/seo.html"
		context = {

					"form":form

				}

		return render(request,template_name,context)

	except:

		return HttpResponseRedirect(reverse('Reporter:enable_settings'))

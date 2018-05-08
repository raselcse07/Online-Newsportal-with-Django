from datetime import timedelta, datetime, date
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import (
                    CategoryCreateForm,
                    PostCreateForm,
                    PostUpdateForm,
                    DivisionalCategoryCreateForm
                    )

from .models import (
                    PostModel,
                    PostCategory,
                    DivisionalPostCategory,
                    DivisionName
                    )
from Gallery.models import ImageGallery
from Reporter.models import Profile
from Homepage.models import (
                            GeneralSettings,
                            InsertHeaderFooter,
                            HomepageMiddleSection,
                            HomepageAds,
                            PostDetailPageAds,
                            CopyRightSection,
                            SEO
                            )
from Homepage.views import CategorySlice
from Instant_Article.models import InstantArticleModel



########################################################################################
#                                   Create views                                       #
########################################################################################

# This method is for ajax call

def load_disticts(request):

    division_id = request.GET.get('division')
    disticts = DivisionalPostCategory.objects.filter(id=division_id)
    return render(request, 'Post/disticts_dropdown_list_options.html', {'disticts': disticts})

def CategoryCreate(request):

    qs = PostCategory.objects.all()
    qs2 = DivisionalPostCategory.objects.all()
    form=CategoryCreateForm(request.POST or None)
    form2 = DivisionalCategoryCreateForm(request.POST or None)

    if form.is_valid() and "general_category" in request.POST:

        instance=form.save(commit=False)
        instance.save()
        messages.success(request, "Category Created", extra_tags='html_safe')

    if form2.is_valid() and "divisonal_category" in request.POST:

        instance=form2.save(commit=False)
        instance.save()
        messages.success(request, "Category Created", extra_tags='html_safe')


    template_name="Post/category_create.html"
    context={
                "form":form,
                "qs":qs,
                "form2":form2,
                "qs2":qs2
            }

    return render(request,template_name,context)

def PostCreateView(request):


    form=PostCreateForm(request.POST or None,request.FILES or None)

    if form.is_valid():


        instance=form.save(commit=False)
        instance.user=request.user
        instance.save()

        messages.success(request, "Post Created", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url() +"edit/")

    template_name="Post/post_create.html"
    context={"form":form}

    return render(request,template_name,context)


#########################################################################################
#                           List & Detail Views                                         #
#########################################################################################

def PostList(request):

    qs=PostModel.objects.all() # Getting all posts
    qs2=ImageGallery.objects.all() # Getting all images
    reporter_name = Profile.objects.all()
    user_post=PostModel.objects.filter(user=request.user)
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)


    try:
        posts_qs = paginator.page(page)
    except PageNotAnInteger:
        posts_qs = paginator.page(1)
    except EmptyPage:
        posts_qs = paginator.page(paginator.num_pages)


    template_name="Post/post_list.html"
    context={

                "posts_qs":posts_qs,
                "qs2":qs2,
                "qs":qs,
                "reporter_name":reporter_name,
                "user_post":user_post
            }

    return render(request,template_name,context)

def PostDetail(request,slug=None):

    qs                  = get_object_or_404(PostModel,slug=slug)
    category_qs         = get_object_or_404(PostCategory,category_name=qs.category)
    featured_image_qs   = get_object_or_404(ImageGallery,image_id=qs.featured_image_id)
    qs.total_page_views += 1
    qs.save()
    total_hit           = qs.total_page_views
    general_settings    = GeneralSettings.objects.all()[0]
    header_footer_code  = InsertHeaderFooter.objects.all()[0] # Header and Footer Code
    all_category        = PostCategory.objects.all() # All category
    reporter            = Profile.objects.get(username=qs.user)
    middle_ads_code     = HomepageMiddleSection.objects.all()[0] # Middle section ads code.Show in right.
    all_posts           = PostModel.objects.all() # All Posts
    most_popular        = PostModel.objects.all().order_by("-total_page_views")
    all_images          = ImageGallery.objects.all() # All Images
    ads_homepage        = HomepageAds.objects.all()[0]
    post_detail_ads     = PostDetailPageAds.objects.all()[0]
    copyright_info		= CopyRightSection.objects.all()[0]
    seo                 = SEO.objects.all()[0]
    google_analytics 	= InstantArticleModel.objects.all()[0]


    '''
    This is the value of all category which is
    divided into two parts first.Then each of
    that parts are again divided into two parts.
    Thus, we have divided the catgory into 4 parts.
    '''

    category_1st_half,category_2nd_half = CategorySlice(all_category)
    category_1st_half_1st = category_1st_half[:len(category_1st_half)//2]
    category_1st_half_2nd = category_1st_half[len(category_1st_half)//2:]
    category_2nd_half_1st = category_2nd_half[:len(category_2nd_half)//2]
    category_2nd_half_2nd = category_2nd_half[len(category_2nd_half)//2:]



    template_name="Post/post_detail.html"


    context={
                "qs":qs,
                "category_qs":category_qs,
                "featured_image_qs":featured_image_qs,
                "total_hit":total_hit,
                "general_settings":general_settings,
                "header_footer_code":header_footer_code,
                "all_category":all_category,
                "category_1st_half_1st":category_1st_half_1st,
                "category_1st_half_2nd":category_1st_half_2nd,
                "category_2nd_half_1st":category_2nd_half_1st,
                "category_2nd_half_2nd":category_2nd_half_2nd,
                "reporter":reporter,
                "middle_ads_code":middle_ads_code,
                "all_posts":all_posts,
                "most_popular":most_popular,
                "all_images":all_images,
                "ads_homepage":ads_homepage,
                "post_detail_ads":post_detail_ads,
                "copyright_info":copyright_info,
                "seo":seo,
                "google_analytics":google_analytics


            }

    return render(request,template_name,context)

def CategoryDetail(request,category_slug=None):

    qs                      = get_object_or_404(PostCategory,category_slug=category_slug)
    post_qs                 = PostModel.objects.filter(category__category_name__exact=qs.category_name)
    featured_image_qs       = ImageGallery.objects.all()
    header_footer_code      = InsertHeaderFooter.objects.all()[0] # Header and Footer Code
    general_settings        = GeneralSettings.objects.all()[0]
    all_category            = PostCategory.objects.all() # All category
    all_posts               = PostModel.objects.all() # All Posts
    most_popular            = PostModel.objects.all().order_by("-total_page_views")
    ads_homepage            = HomepageAds.objects.all()[0],
    copyright_info		    = CopyRightSection.objects.all()[0]
    seo                     = SEO.objects.all()[0]
    google_analytics 	    = InstantArticleModel.objects.all()[0]



    page = request.GET.get('page', 1)

    paginator = Paginator(post_qs, 18)


    try:
        paginator_qs = paginator.page(page)
    except PageNotAnInteger:
        paginator_qs = paginator.page(1)
    except EmptyPage:
        paginator_qs = paginator.page(paginator.num_pages)


    '''
    This is the value of all category which is
    divided into two parts first.Then each of
    that parts are again divided into two parts.
    Thus, we have divided the catgory into 4 parts.
    '''

    category_1st_half,category_2nd_half = CategorySlice(all_category)
    category_1st_half_1st               = category_1st_half[:len(category_1st_half)//2]
    category_1st_half_2nd               = category_1st_half[len(category_1st_half)//2:]
    category_2nd_half_1st               = category_2nd_half[:len(category_2nd_half)//2]
    category_2nd_half_2nd               = category_2nd_half[len(category_2nd_half)//2:]

    template_name="Post/category_detail.html"
    context={
                "qs":qs,
                "post_qs":post_qs,
                "featured_image_qs":featured_image_qs,
                "header_footer_code":header_footer_code,
                "general_settings":general_settings,
                "all_category":all_category,
                "category_1st_half_1st":category_1st_half_1st,
                "category_1st_half_2nd":category_1st_half_2nd,
                "category_2nd_half_1st":category_2nd_half_1st,
                "category_2nd_half_2nd":category_2nd_half_2nd,
                "paginator_qs":paginator_qs,
                "all_posts":all_posts,
                "most_popular":most_popular,
                "ads_homepage":ads_homepage,
                "copyright_info":copyright_info,
                "seo":seo,
                "google_analytics":google_analytics

            }

    return render(request,template_name,context)

#####################################################################################
#                               Update & Delete Views                               #
#####################################################################################

def PostUpdate(request,slug=None):

    qs=get_object_or_404(PostModel,slug=slug)
    form=PostUpdateForm(request.POST or None,request.FILES or None,instance=qs)
    featured_image_qs=get_object_or_404(ImageGallery,image_id=qs.featured_image_id)

    if form.is_valid():

        instance=form.save(commit=False)
        instance.save()
        messages.success(request, "Post Updated", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url() +"edit/")

    template_name="Post/post_update.html"
    context={

        "form":form,
        "qs":qs,
        "featured_image_qs":featured_image_qs

    }

    return render(request,template_name,context)

def PostDetele(request,slug=None):

    instance=get_object_or_404(PostModel,slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted", extra_tags='html_safe')
    return redirect("Post:post_list")


def about_views(request):

    about_string            = CopyRightSection.objects.all()
    general_settings        = GeneralSettings.objects.all()[0]
    all_category            = PostCategory.objects.all() # All category
    copyright_info			= CopyRightSection.objects.all()[0]
    header_footer_code      = InsertHeaderFooter.objects.all()[0] # Header and Footer Code


    '''
    This is the value of all category which is
    divided into two parts first.Then each of
    that parts are again divided into two parts.
    Thus, we have divided the catgory into 4 parts.
    '''

    category_1st_half,category_2nd_half = CategorySlice(all_category)
    category_1st_half_1st = category_1st_half[:len(category_1st_half)//2]
    category_1st_half_2nd = category_1st_half[len(category_1st_half)//2:]
    category_2nd_half_1st = category_2nd_half[:len(category_2nd_half)//2]
    category_2nd_half_2nd = category_2nd_half[len(category_2nd_half)//2:]

    template_name ="Homepage/about.html"

    context = {

        "about_string":about_string,
        "general_settings":general_settings,
        "all_category":all_category,
        "category_1st_half_1st":category_1st_half_1st,
        "category_1st_half_2nd":category_1st_half_2nd,
        "category_2nd_half_1st":category_2nd_half_1st,
        "category_2nd_half_2nd":category_2nd_half_2nd,
        "copyright_info":copyright_info,
        "header_footer_code":header_footer_code

	}

    return render(request,template_name,context)


def contact_views(request):

    about_string            = CopyRightSection.objects.all()
    general_settings        = GeneralSettings.objects.all()[0]
    all_category            = PostCategory.objects.all() # All category
    copyright_info			= CopyRightSection.objects.all()[0]
    header_footer_code      = InsertHeaderFooter.objects.all()[0] # Header and Footer Code


    '''
    This is the value of all category which is
    divided into two parts first.Then each of
    that parts are again divided into two parts.
    Thus, we have divided the catgory into 4 parts.
    '''

    category_1st_half,category_2nd_half = CategorySlice(all_category)
    category_1st_half_1st = category_1st_half[:len(category_1st_half)//2]
    category_1st_half_2nd = category_1st_half[len(category_1st_half)//2:]
    category_2nd_half_1st = category_2nd_half[:len(category_2nd_half)//2]
    category_2nd_half_2nd = category_2nd_half[len(category_2nd_half)//2:]

    template_name ="Homepage/contact.html"

    context = {

        "about_string":about_string,
        "general_settings":general_settings,
        "all_category":all_category,
        "category_1st_half_1st":category_1st_half_1st,
        "category_1st_half_2nd":category_1st_half_2nd,
        "category_2nd_half_1st":category_2nd_half_1st,
        "category_2nd_half_2nd":category_2nd_half_2nd,
        "copyright_info":copyright_info,
        "header_footer_code":header_footer_code

	}

    return render(request,template_name,context)

def privacy_views(request):

    about_string            = CopyRightSection.objects.all()
    general_settings        = GeneralSettings.objects.all()[0]
    all_category            = PostCategory.objects.all() # All category
    copyright_info			= CopyRightSection.objects.all()[0]
    header_footer_code      = InsertHeaderFooter.objects.all()[0] # Header and Footer Code


    '''
    This is the value of all category which is
    divided into two parts first.Then each of
    that parts are again divided into two parts.
    Thus, we have divided the catgory into 4 parts.
    '''

    category_1st_half,category_2nd_half = CategorySlice(all_category)
    category_1st_half_1st = category_1st_half[:len(category_1st_half)//2]
    category_1st_half_2nd = category_1st_half[len(category_1st_half)//2:]
    category_2nd_half_1st = category_2nd_half[:len(category_2nd_half)//2]
    category_2nd_half_2nd = category_2nd_half[len(category_2nd_half)//2:]

    template_name ="Homepage/privacy.html"

    context = {

        "about_string":about_string,
        "general_settings":general_settings,
        "all_category":all_category,
        "category_1st_half_1st":category_1st_half_1st,
        "category_1st_half_2nd":category_1st_half_2nd,
        "category_2nd_half_1st":category_2nd_half_1st,
        "category_2nd_half_2nd":category_2nd_half_2nd,
        "copyright_info":copyright_info,
        "header_footer_code":header_footer_code

	}

    return render(request,template_name,context)

def advertisements_views(request):

    about_string            = CopyRightSection.objects.all()
    general_settings        = GeneralSettings.objects.all()[0]
    all_category            = PostCategory.objects.all() # All category
    copyright_info			= CopyRightSection.objects.all()[0]
    header_footer_code      = InsertHeaderFooter.objects.all()[0] # Header and Footer Code


    '''
    This is the value of all category which is
    divided into two parts first.Then each of
    that parts are again divided into two parts.
    Thus, we have divided the catgory into 4 parts.
    '''

    category_1st_half,category_2nd_half = CategorySlice(all_category)
    category_1st_half_1st = category_1st_half[:len(category_1st_half)//2]
    category_1st_half_2nd = category_1st_half[len(category_1st_half)//2:]
    category_2nd_half_1st = category_2nd_half[:len(category_2nd_half)//2]
    category_2nd_half_2nd = category_2nd_half[len(category_2nd_half)//2:]

    template_name ="Homepage/adsvertisements.html"

    context = {

        "about_string":about_string,
        "general_settings":general_settings,
        "all_category":all_category,
        "category_1st_half_1st":category_1st_half_1st,
        "category_1st_half_2nd":category_1st_half_2nd,
        "category_2nd_half_1st":category_2nd_half_1st,
        "category_2nd_half_2nd":category_2nd_half_2nd,
        "copyright_info":copyright_info,
        "header_footer_code":header_footer_code

	}

    return render(request,template_name,context)

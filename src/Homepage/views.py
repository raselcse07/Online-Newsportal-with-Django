from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from Post.models import PostModel,PostCategory,DivisionalPostCategory
from Gallery.models import ImageGallery
from .models import (
					HomepageMiddleSection,
					InsertHeaderFooter,
					HomepageMiddleSectionBelow,
					HomepageMiddleSectionBelowTwo,
					FooterAboveSection,
					GeneralSettings,
					HomepageAds,
					CopyRightSection,
					SEO
					)
from Instant_Article.models import InstantArticleModel


def CategorySlice(category_query):
	# This function will split the all category into two parts.
	category_list = []
	for i in category_query:
		category_list.append(i.category_name)
		half = len(category_list)//2
	return category_list[:half],category_list[half:]




def homepage_views(request):

	# try:



		latest_post					= PostModel.objects.all()[:6] # Last 6 Posts
		all_category				= PostCategory.objects.all() # All category
		all_posts 					= PostModel.objects.all() # All Posts
		all_images 					= ImageGallery.objects.all() # All Images
		middle_section 				= HomepageMiddleSection.objects.all() # All Selected Middle Section Category
		middle_left_category 		= PostCategory.objects.get(category_name=middle_section[0].part_one_left) # Middle left category name
		middle_right_category 		= PostCategory.objects.get(category_name=middle_section[0].part_two_right)# Middle right(center) category name
		middle_left_all_post 		= PostModel.objects.filter(category=middle_left_category)[1:4] # Middle left category posts (last 3 posts without first post)
		middle_left_first_post 		= PostModel.objects.filter(category=middle_left_category)[0] # Middle left category latest post
		middle_right_all_post 		= PostModel.objects.filter(category=middle_right_category)[1:4] # Middle right(center) posts.
		middle_right_first_post 	= PostModel.objects.filter(category=middle_right_category)[0] # Middle right(center) latest post.
		middle_ads_code				= HomepageMiddleSection.objects.all()[0] # Middle section ads code.Show in right.
		header_footer_code 			= InsertHeaderFooter.objects.all()[0] # Header and Footer Code
		middle_section_below		= HomepageMiddleSectionBelow.objects.all() # Section immediate below of middle section.Get that category.
		middle_section_below_posts	= PostModel.objects.filter(category=middle_section_below[0].part_one)[1:5] # All posts of selected section of immediate below of middle.Latest 4 posts(without last post)
		middle_section_below_posts_1= PostModel.objects.filter(category=middle_section_below[0].part_one)[0] # Thats the latest post.
		middle_section_below_cat	= PostCategory.objects.get(category_name=middle_section_below[0].part_one) # Category name of immediate below of middle.
		middle_below_two			= HomepageMiddleSectionBelowTwo.objects.all() # Third middle section category.
		middle_below_two_post		= PostModel.objects.filter(category=middle_below_two[0].part_one_two)[1:7] # Third middle section posts
		middle_below_two_post_1		= PostModel.objects.filter(category=middle_below_two[0].part_one_two)[0] # Third middle section clatest post.
		middle_below_two_cat 		= PostCategory.objects.get(category_name=middle_below_two[0].part_one_two) # Third middle section category name.
		footer_above				= FooterAboveSection.objects.all() # footer category
		footer_above_cat_1_name		= PostCategory.objects.get(category_name=footer_above[0].footer_above_1) # Footer 1 category name
		footer_above_1_posts		= PostModel.objects.filter(category=footer_above_cat_1_name)[:4] # Footer 1 posts.
		footer_above_cat_2_name		= PostCategory.objects.get(category_name=footer_above[0].footer_above_2) # Footer 2 category name
		footer_above_2_posts		= PostModel.objects.filter(category=footer_above_cat_2_name)[:4] # Footer 2 posts.
		footer_above_cat_3_name		= PostCategory.objects.get(category_name=footer_above[0].footer_above_3) # Footer 3 category name
		footer_above_3_posts		= PostModel.objects.filter(category=footer_above_cat_3_name)[:4] # Footer 3 posts.
		footer_above_cat_4_name		= PostCategory.objects.get(category_name=footer_above[0].footer_above_4) # Footer 4 category name
		footer_above_4_posts		= PostModel.objects.filter(category=footer_above_cat_4_name)[:4] # Footer 4 posts.
		general_settings			= GeneralSettings.objects.all()[0]
		most_popular				= PostModel.objects.all().order_by("-total_page_views")
		ads_homepage				= HomepageAds.objects.all()[0]
		copyright_info				= CopyRightSection.objects.all()[0]
		seo 						= SEO.objects.all()[0]
		google_analytics 			= InstantArticleModel.objects.all()[0]


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

		template_name = "Homepage/index.html"
		context ={

				"latest_post":latest_post,
				"all_posts":all_posts,
				"all_images":all_images,
				"all_category":all_category,
				"middle_section":middle_section,
				"middle_left_category":middle_left_category,
				"middle_right_category":middle_right_category,
				"middle_left_all_post":middle_left_all_post,
				"middle_left_first_post":middle_left_first_post,
				"middle_right_all_post":middle_right_all_post,
				"middle_right_first_post":middle_right_first_post,
				"middle_ads_code":middle_ads_code,
				"header_footer_code":header_footer_code,
				"middle_section_below_posts":middle_section_below_posts,
				"middle_section_below_posts_1":middle_section_below_posts_1,
				"middle_section_below_cat":middle_section_below_cat,
				"middle_below_two_post":middle_below_two_post,
				"middle_below_two_post_1":middle_below_two_post_1,
				"middle_below_two_cat":middle_below_two_cat,
				"footer_above_cat_1_name":footer_above_cat_1_name,
				"footer_above_1_posts":footer_above_1_posts,
				"footer_above_cat_2_name":footer_above_cat_2_name,
				"footer_above_2_posts":footer_above_2_posts,
				"footer_above_cat_3_name":footer_above_cat_3_name,
				"footer_above_3_posts":footer_above_3_posts,
				"footer_above_cat_4_name":footer_above_cat_4_name,
				"footer_above_4_posts":footer_above_4_posts,
				"category_1st_half_1st":category_1st_half_1st,
				"category_1st_half_2nd":category_1st_half_2nd,
				"category_2nd_half_1st":category_2nd_half_1st,
				"category_2nd_half_2nd":category_2nd_half_2nd,
				"general_settings":general_settings,
				"most_popular":most_popular,
				"ads_homepage":ads_homepage,
				"copyright_info":copyright_info,
				"seo":seo,
				"google_analytics":google_analytics
		}

		return render(request,template_name,context)

	# except:
	# 	raise Http404

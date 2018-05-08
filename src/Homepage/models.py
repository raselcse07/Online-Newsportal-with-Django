from django.db import models
from Post.models import PostCategory



def upload_location_site_logo(instance, filename):

	return "Site Logo/%s/%s" %(instance.name_of_site,filename)

def upload_location_site_fav(instance, filename):

	return "Site Favicon/%s/%s" %(instance.name_of_site,filename)

class HomepageMiddleSection(models.Model):

	part_one_left		= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1,related_name="Left")
	part_two_right 		= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1,related_name="Middle")
	ads_code_1			= models.TextField(default="",blank=True)
	ads_code_2 			= models.TextField(default="",blank=True)
	fb_page_code 		= models.TextField(default="",blank=True,help_text="You will get page plugin from <a href='https://developers.facebook.com/docs/plugins/page-plugin/' target='_blank'>here.</a>")



	def __str__(self):

		return "Middle Widget"

class InsertHeaderFooter(models.Model):


	header_code 		= models.TextField(default="",blank=True)
	footer_code 		= models.TextField(default="",blank=True)


	def __str__(self):

		return "Insert Header & Footer"

class HomepageMiddleSectionBelow(models.Model):

	part_one 			= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1)


	def __str__(self):

		return "Middle Widget Below"

class HomepageMiddleSectionBelowTwo(models.Model):

	part_one_two 			= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1)


	def __str__(self):

		return "Middle Widget Below Two"

class FooterAboveSection(models.Model):

	footer_above_1			= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1,related_name="footer_above_1")
	footer_above_2			= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1,related_name="footer_above_2")
	footer_above_3			= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1,related_name="footer_above_3")
	footer_above_4			= models.ForeignKey(PostCategory,on_delete=models.CASCADE,default=1,related_name="footer_above_4")


	def __str__(self):

		return "Footer Above Section"

class GeneralSettings(models.Model):

	name_of_site 			= models.CharField(max_length=200,blank=True)
	site_tag_line			= models.CharField(max_length=200,blank=True)
	site_logo				= models.ImageField(upload_to=upload_location_site_logo,
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field")
	height_field        	= models.IntegerField(default=0)
	width_field         	= models.IntegerField(default=0)
	site_favicon			= models.ImageField(upload_to=upload_location_site_fav,
                                null=True,
                                blank=True,
                                width_field="height_field_fav",
                                height_field="width_field_fav")
	height_field_fav        = models.IntegerField(default=32)
	width_field_fav         = models.IntegerField(default=32)

	def __str__(self):
		return str(self.name_of_site)


class HomepageAds(models.Model):

	header_ads_970x90		= models.TextField(default="",blank=True)
	sidebar_1				= models.TextField(default="",blank=True)
	sidebar_2				= models.TextField(default="",blank=True)
	sidebar_3				= models.TextField(default="",blank=True)

	def __str__(self):

		return "Homepage Ads"

class PostDetailPageAds(models.Model):

	left_sidebar_160x900	= models.TextField(default="",blank=True)
	right_sidebar_1			= models.TextField(default="",blank=True)
	right_sidebar_2			= models.TextField(default="",blank=True)
	right_sidebar_3			= models.TextField(default="",blank=True)
	before_post				= models.TextField(default="",blank=True)
	after_post				= models.TextField(default="",blank=True)

	def __str__(self):

		return "Post Detail Ads"

class CopyRightSection(models.Model):

	copy_right_text			= models.TextField(default="",blank=True)
	about_summary			= models.TextField(default="",blank=True)
	about_full				= models.TextField(default="",blank=True)
	editor_email			= models.CharField(max_length=250,default="",blank=True)
	privary_policy			= models.TextField(default="",blank=True)
	conatct					= models.TextField(default="",blank=True)
	advertisement			= models.TextField(default="",blank=True)


	def __str__(self):

		return "Copyright Section"


class SEO(models.Model):

	facebook_app_id			= models.CharField(max_length=200,verbose_name = "Facebook App ID",default="",blank=True)
	facebook_page_id		= models.CharField(max_length=200,verbose_name = "Facebook Page ID",default="",blank=True)
	meta_description		= models.TextField(default="",verbose_name="Meta Description",blank=True)
	domain_name				= models.CharField(max_length=200,verbose_name = "Domain Name",default="",blank=True)
	site_title				= models.CharField(max_length=200,verbose_name = "Site Title",default="",blank=True)


	def __str__(self):

		return "SEO"


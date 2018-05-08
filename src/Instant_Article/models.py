from django.db import models
from django.utils.safestring import mark_safe




class InstantArticleModel(models.Model):

	facebook_page_ID		= models.CharField(max_length=200,verbose_name="Facebook Page ID",default="",blank=True)
	article_style			= models.CharField(max_length=200,verbose_name="Article Style",default="",blank=True)
	copyright				= models.CharField(max_length=200,verbose_name="Copyright",default="",blank=True)
	domain_name				= models.CharField(max_length=200,verbose_name="Domain Name",default="",blank=True)
	ads_code				= models.CharField(max_length=200,verbose_name="Ads Code",default="",blank=True)
	google_analytics		= models.TextField(verbose_name="Google Analytics Code",default="",blank=True)


	def __str__(self):

		return "Instant Article"

	@property
	def get_markdown(self):
		content = self.copyright
		return mark_safe(content)

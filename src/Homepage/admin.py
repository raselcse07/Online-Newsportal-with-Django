from django.contrib import admin
from .models import (
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


admin.site.register(HomepageMiddleSection)
admin.site.register(InsertHeaderFooter)
admin.site.register(HomepageMiddleSectionBelow)
admin.site.register(HomepageMiddleSectionBelowTwo)
admin.site.register(FooterAboveSection)
admin.site.register(GeneralSettings)
admin.site.register(HomepageAds)
admin.site.register(PostDetailPageAds)
admin.site.register(CopyRightSection)
admin.site.register(SEO)

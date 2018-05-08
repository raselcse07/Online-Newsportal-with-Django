import re
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.xmlutils import SimplerXMLGenerator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from Post.models import PostModel
from Homepage.models import GeneralSettings
from Gallery.models import ImageGallery
from Reporter.models import Profile
from .models import InstantArticleModel


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = ['</p><p><img style="width: 623px;" src=','jpg"><br></p>']
    s = s.replace(htmlCodes[0], "<figure><img src=")
    s = s.replace(htmlCodes[1],'jpg"><figure>')

    return s

class UnescapedXMLGenerator(SimplerXMLGenerator):

    def characters(self, content):
        """
        code is mainly copy-paste from Django 1.10 SimplerXMLGenerator.characters
        """
        if content and re.search(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', content):
            # Fail loudly when content has control chars (unsupported in XML 1.0)
            # See http://www.w3.org/International/questions/qa-controls
            raise UnserializableContentError("Control characters are not supported in XML 1.0")

        # next part from sax.saxutils.XMLGenerator, but without escaping
        if not isinstance(content, str):
            content = unicode(content, self._encoding)
        self._write(content)


class ExtendedRSSFeed(Rss201rev2Feed):

    def write(self, outfile, encoding):
        """
        code is mainly copy-paste from django.utils.feedgenerator.Rss201rev2Feed
        except that the handler is set to UnescapedXMLGenerator
        """
        handler = UnescapedXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement("rss", self.rss_attributes())
        handler.startElement("channel", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement("rss")


    def rss_attributes(self):
        attrs=super(ExtendedRSSFeed,self).rss_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs


    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])

class LatestEntriesFeed(Feed):

    general_settings = GeneralSettings.objects.all()[0]

    title = general_settings.name_of_site + " - Instant Articles"
    link = "/"
    description = general_settings.site_tag_line

    feed_type = ExtendedRSSFeed

    def items(self):
        return PostModel.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return Truncator(strip_tags(item.get_markdown)).words(30)

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('Post:post_detail', kwargs={"slug":item.slug})

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    def item_content_encoded(self, item):

        qs = InstantArticleModel.objects.all()[0]
        url = qs.domain_name+reverse('Post:post_detail', kwargs={"slug":item.slug})
        title = item.title
        description = Truncator(strip_tags(item.get_markdown)).words(30)
        image_qs = get_object_or_404(ImageGallery,image_id=item.featured_image_id)
        image_url = qs.domain_name+image_qs.upload_image.url
        style =qs.article_style
        timestamp = item.timestamp
        formated_timestamp = timestamp.strftime("%Y-%m-%d %H:%M %p")
        updated = item.updated
        formated_updated = timestamp.strftime("%Y-%m-%d %H:%M %p")
        category = item.category
        user = Profile.objects.get(username=item.user).display_name
        ads_code=qs.ads_code
        content = html_decode(item.get_markdown)
        google_analytics_code =qs.google_analytics
        copyright_text = qs.get_markdown

        html = '''
                <!doctype html>
                    <html lang="en" prefix="op: http://media.facebook.com/op#">
                      <head>
                        <meta charset="utf-8">
                        <link rel="canonical" href="{url}">
                        <meta property="og:url" content="{url2}" />
                        <meta property="og:type" content="article" />
                        <meta property="og:title" content="{title}" />
                        <meta property="og:description" content="{description}" />
                        <meta property="og:image" content="{image_qs}" />
                        <meta property="op:markup_version" content="v1.0">
                        <meta property="fb:use_automatic_ad_placement" content="enable=true ad_density=default"/>
                        <meta property="fb:article_style" content="{style}"/>
                      </head>
                      <body>
                        <article>
                          <header>
                             <figure><img src="{post_image}"/></figure>
                             <h1>{title2}</h1>
                             <time class="op-published" datetime="{timestamp1}">{timestamp2}</time><time class="op-modified" datetime="{updated1}">{updated2}</time>
                             <address><a>{user}</a></address>
                             <h3 class="op-kicker">{category}</h3>
                             <figure class="op-ad"><iframe src="https://www.facebook.com/adnw_request?placement={ads_code}&amp;adtype=banner300x250" width="300" height="250"></iframe></figure>
                          </header>
                            {content}
                            <figure class="op-tracker">
                                <iframe>
                                    {google_analytics_code}
                                </iframe>
                            </figure>

                          <footer>
                            <small>{copyright_text}</small>
                          </footer>
                        </article>
                      </body>
                    </html>

                '''.format(
                        url=url,
                        url2=url,
                        title=title,
                        description=description,
                        image_qs=image_url,
                        style=style,
                        post_image=image_url,
                        timestamp1=timestamp,
                        timestamp2=formated_timestamp,
                        updated1 = updated,
                        updated2 = formated_updated,
                        category=category,
                        user=user,
                        ads_code=ads_code,
                        content=content,
                        title2=title,
                        google_analytics_code = google_analytics_code,
                        copyright_text=copyright_text
                        )

        return html_decode("<![CDATA[%s]]>" % html)

import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_category_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = "-".join(instance.category_name.split())

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(category_slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_category_slug_generator(instance, new_slug=new_slug)
    return slug

def unique_divisional_category_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = "-".join(instance.name_of_distict.split())

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(divisional_category_slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_divisional_category_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_post_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = "-".join(instance.title.split())

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_post_slug_generator(instance, new_slug=new_slug)
    return slug

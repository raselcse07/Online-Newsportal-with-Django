import os
from django.conf import settings
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from .forms import ImageUplaodForm
from .models import ImageGallery
from django.conf import settings

def ImageUpload(request):

    q=request.GET.get("q", None)
    qs=ImageGallery.objects.all().order_by("-id")
    form=ImageUplaodForm(request.POST or None,request.FILES or None)
    images_in_root=os.listdir(settings.MEDIA_ROOT)

    page = request.GET.get('page', 1)

    paginator = Paginator(images_in_root, 5)


    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)



    if q is not None:

        qs = qs.filter(Q(image_title__icontains=q)|Q(upload_image__icontains=q))


    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request, "Image Uploaded", extra_tags='html_safe')

    template_name="Gallery/image_upload.html"
    context={
        "form":form,
        "qs":qs,
        "images":images
    }

    return render(request,template_name,context)

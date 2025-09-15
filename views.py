from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .utils import download_youtube_video

@login_required
def import_youtube(request):
    if request.method == "POST":
        url = request.POST.get('url')
        media_list = download_youtube_video(url, request.user)
        if not media_list:
            # No media downloaded, show an error or redirect
            return render(request, "form.html", {"error": "No media downloaded."})

        first_media = media_list[0]
        return redirect(first_media.get_absolute_url())

    return render(request, "form.html")

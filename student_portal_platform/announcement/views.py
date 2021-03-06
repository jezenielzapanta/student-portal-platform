from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse

from .models import GlobalAnnouncement
from .forms import AnnouncementForm


@login_required
def announcement_post(request):
    if request.method == "GET":
        return render(request, 'proto_design/announce-post.html',
                      { 'announcementForm' : AnnouncementForm()})
        
    elif request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = GlobalAnnouncement.objects.create(title = form.cleaned_data['title'],
                                                       content = form.cleaned_data['content'],
                                                       author = request.user)
            return HttpResponse("you posted")
        
def announcement_view(request, post_id):
    announcement = get_object_or_404(GlobalAnnouncement, id=post_id)
    return render(request, 'proto_design/announce-view.html', {'announcement': announcement})

@login_required
def announcement_profile(request):
    try:
        announcements = GlobalAnnouncement.objects.all()
    except GlobalAnnouncement.DoesNotExist:
        announcements = None
    return render(request,"official/announcement.html", {'announcements': announcements })

def announcement_list(request, page_num = 5):
    announce_list = GlobalAnnouncement.objects.order_by("-postdate")
    paginator = Paginator(announce_list, page_num)
    
    page = request.GET.get("page")
    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)
    return render_to_response("proto_design/announcements.html", {'announcements':announcements})
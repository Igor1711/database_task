from django.conf.urls import url
from api import views

urlpatterns = [
	url(r'^clear/', views.clear, name="clear"),
	url(r'^status/', views.status, name="status"),
	url(r'^forum/create/', views.forumcreate, name="forumcreate"),
	url(r'^forum/details/',views.forumdetails, name="forumdetails"),
	url(r'^forum/listPosts/', views.forumlistposts, name="forumlistposts"),
	url(r'^forum/listThreads/', views.forumlistthreads, name="forumlistthreads"),
	url(r'^forum/listUsers/', views.forumlistusers, name="forumlistusers"),
	url(r'^post/create/', views.postcreate, name="postcreate"),
	url(r'^post/details/', views.postdetails, name="postdetails"),
	url(r'^post/list/', views.postlist, name="postdetails"),
	url(r'^post/remove/', views.postremove, name="postremove"),
        url(r'^post/restore/', views.postrestore, name="postrestore"),
        url(r'^post/update/', views.postupdate, name="postupdate"),
        url(r'^post/vote/', views.postvote, name="postvote"),
	url(r'^user/create/', views.usercreate, name="usercreate"),
	url(r'^user/details/', views.userdetails, name="userdetails"),
        url(r'^user/follow/', views.userfollow, name="userfollow"),
        url(r'^user/listFollowers/', views.userlistfollowers, name="userlistfollowers"),
        url(r'^user/listFollowing/', views.userlistfollowing, name="userlistfollowing"),
        url(r'^user/listPosts/', views.userlistposts, name="userlistposts"),
        url(r'^user/unfollow/', views.userunfollow, name="userunfollow"),
	url(r'^user/updateProfile/', views.userupdateprofile, name="userupdateprofile"),
	url(r'^thread/close/' , views.threadclose, name="threadclose"),
	url(r'^thread/create/' , views.threadcreate, name="threadcreate"),
	url(r'^thread/details/' , views.threaddetails, name="threaddetails"),
	url(r'^thread/list/' , views.threadlist, name="threadlist"),
	url(r'^thread/listPosts/' , views.threadlistposts, name="threadlistposts"),
	url(r'^thread/open/' , views.threadopen, name="threadopen"),
	url(r'^thread/remove/' , views.threadremove, name="threadremove"),
	url(r'^thread/restore/' , views.threadrestore, name="threadrestore"),
	url(r'^thread/subscribe/' , views.threadsubscribe, name="threadsubscribe"),
	url(r'^thread/unsubscribe/' , views.threadunsubscribe, name="threadunsubscribe"),
	url(r'^thread/update/' , views.threadupdate, name="threadupdate"),
	url(r'^thread/vote/' , views.threadvote, name="threadvote"),	
]

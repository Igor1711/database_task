from django.shortcuts import render
from django.http import HttpResponse
def clear(request):

	if request.method == "POST":
		return HttpResponse("200 OK")
	else: 
		return HttpResponse("FORBIDDEN")
def status(request):
	return HttpResponse("200 OK")

def forumcreate(request):

	return HttpResponse("200 OK")

def forumdetails(request):

        return HttpResponse("200 OK")
def forumlistposts(request):

        return HttpResponse("200 OK")
def forumlistthreads(request):

        return HttpResponse("200 OK")
def forumlistusers(request):

        return HttpResponse("200 OK")
def postcreate(request):

        return HttpResponse("200 OK")
def postdetails(request):

        return HttpResponse("200 OK")
def postlist(request):

        return HttpResponse("200 OK")
def postremove(request):

        return HttpResponse("200 OK")
def postrestore(request):

        return HttpResponse("200 OK")
def postupdate(request):

        return HttpResponse("200 OK")
def postvote(request):

        return HttpResponse("200 OK")

def usercreate(request):

        return HttpResponse("200 OK")

def userdetails(request):

        return HttpResponse("200 OK")

def userfollow(request):

        return HttpResponse("200 OK")

def userlistfollowers(request):

        return HttpResponse("200 OK")

def userlistfollowing(request):

        return HttpResponse("200 OK")

def userlistposts(request):

        return HttpResponse("200 OK")

def userunfollow(request):

        return HttpResponse("200 OK")

def userupdateprofile(request):

        return HttpResponse("200 OK")

def threadclose(request):

        return HttpResponse("200 OK")

def threadcreate(request):

        return HttpResponse("200 OK")

def threaddetails(request):

        return HttpResponse("200 OK")

def threadlist(request):

        return HttpResponse("200 OK")

def threadlistposts(request):

        return HttpResponse("200 OK")
def threadopen(request):

        return HttpResponse("200 OK")
def threadremove(request):

        return HttpResponse("200 OK")
def threadrestore(request):

        return HttpResponse("200 OK")
def threadsubscribe(request):

        return HttpResponse("200 OK")
def threadunsubscribe(request):

        return HttpResponse("200 OK")
def threadupdate(request):

        return HttpResponse("200 OK")
def threadvote(request):

        return HttpResponse("200 OK")




# Create your views here.

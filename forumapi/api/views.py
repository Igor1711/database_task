from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection, transaction
from jsonview.decorators import json_view

def clear(request):

	if request.method == "POST":
		database=connection.cursor()
		forum.execute("DELETE from FORUM")
		forum.execute("delete from POST")
		forum.execute("delete from USER")
		forum.execute("delete from THREAD")
		return HttpResponse("OK")
	else: 
		
		forum=connection.cursor()
		forum.execute("SELECT name from FORUM")
		output=forum.fetchall()
		return HttpResponse(output)
@json_view
def status(request):
	
	if request.method == "GET":
		numbers=connection.cursor()
		numbers.execute("select COUNT(*) from FORUM")
		user=numbers.fetchone()
#		numbers.execute("select COUNT(*) from THREAD")
		thread=numbers.fetchone()
#		numbers.execute("select COUNT(*) from FORUM")
		forum=numbers.fetchone()
#		numbers.execute("select COUNT(*) from POST")
		post=numbers.fetchone()
		response1= {
			"code":0,
			"response":{
				"user":user,
				"forum":forum,
				"post":post,
				"thread":thread,
			}
		}
		return response1
	else:
		 return HttpResponse("FORBIDDEN")

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

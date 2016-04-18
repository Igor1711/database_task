from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection, transaction
from django.core.serializers import serialize
from json import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet

class MyJsonEncoder(JSONEncoder):
	def encodesery(self, obj):
		if isinstance(obj, QuerySet):
			return loads(serialize('json', obj))
		return JSONEncoder.default(self,obj)
	
def changedictuser(user):
	user1=user
	follow=connection.cursor()
	follow.execute("select user1 from FOLLOW where user2=%s",[user1.get("email")])
	user1["following"]=dumps(follow)
	follow.execute("select user2 from FOLLOW where user1=%s",[user1.get("email")])
	user1["followers"]=dumps(follow.fetchall())
	follow.execute("select threadid from SUBSCRIPTION where user=%s",[user1.get("email")])
	user1["subscription"]=dumps(follow.fetchall())
	return user1

def dictfetchall(cursor, change):
	columns=[col[0] for col in cursor.description]
	if change is None:
		result= [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]
	if change=="user":
		result=[
			changedictuser(dict(zip(columns, row)))
			for row in cursor.fetchall()
		]
	return result	


def clear(request):

	if request.method == "POST":
		database=connection.cursor()
		forum.execute("DELETE from FORUM")
		forum.execute("delete from POST")
		forum.execute("delete from USER")
		forum.execute("delete from THREAD")
		response={
			"code": 0,
			"response":"OK"
		}
		return HttpResponse(dumps(response))
	else: 
		response={
                        "code": 3,
                        "response":"error POST method required"
                }

		return HttpResponse(dumps(response))

def status(request):
	
	if request.method == "GET":
		numbers=connection.cursor()
		numbers.execute("select COUNT(*) from FORUM")
		user=numbers.fetchone()
		numbers.execute("select COUNT(*) from THREAD")
		thread=numbers.fetchone()
		numbers.execute("select COUNT(*) from FORUM")
		forum=numbers.fetchone()
		numbers.execute("select COUNT(*) from POST")
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
		return HttpResponse(dumps(response1))
	else:
		response1={
			"code":3,
			"response":"error GET method required"
		}
		return HttpResponse(dumps(response1))

def forumcreate(request):

	if request.method == "POST":
		name=request.POST.get("name")
		short_name=request.get("short_name")
		user=request.get("user")
		if name is None or short_name is None or user is None:
			response={"code":2,"response":"Invalid request"}
			return HttpResponse(dumps(response))
		else:

			new_forum=connection.cursor()
			new_forum.execute("insert into FORUM(name,short_name,user) values("+name+","+short_name+","+user+")")
			new_forum.execute("select ID as id,name,short_name,user from FORUM where name like %s and short_name like %s and user like %s",[name,short_name,user])
			response=dictfetchall(new_forum)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
	else:
		response={"code":3,"response":"error POST method required"}
		return HttpResponse(dumps(response))

def forumdetails(request):
	if request.method == "GET":
		short_name=request.GET.get("forum")
		related=request.GET.get("related")
		if short_name is None:
			response={"code":2,"response":"Invalid request, forum name required"}
			return HttpResponse(dumps(response))
		details=connection.cursor()
		if related is None:
			details.execute('select ID as id, name, short_name, user from FORUM where short_name like %s group by short_name',[short_name])
		else:
			details.execute("select ID as id, name, short_name, (select about,email,id,isAnonymous,name,username from USER where email like %s) as user from FORUM where short_name=%s",[short_name,"test_user@mail.ru"])
		response=dictfetchall(details)
		if dumps(response)==[] is None:
			response1={"code":0,"response":"forum "+short_name+" does not exist"}
		else:
			response1={"code":0, "response":response}
		return HttpResponse(dumps(response1))
	else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))

       
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

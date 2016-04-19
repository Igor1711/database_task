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
	
def relateddict(dict1, relate)
	if change is None:
		return dict1
	else: 
		forum=false
		user=false
		thread=flase
		for element in relate:
			if element=="forum":
				forum=true
			if element=="user":
				user=true
			if element=="thread":
				thread=true
		if forum==true or user==true or thread=true:
			realtion=connection.cursor()
			if forum == true:
				relation.execute("select ID as id, name,short_name,user from FORUM where short_name=%s",[dict1[forum]])
				dict1[forum]=relation(dictfetchall(relation,None))
			if user == true:
				relation.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER, where email=%s", [dict1[user]])
				dict1[user]=relation(dictfetchall(relation,"user"))
			if thread == true:
				relation.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID ad id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select count(*) from POST where thread=THREAD.ID) as posts slug, title, user from THREAD where ID="+dict1[thread])
				dict1[thread]=relation(dictfetchall(relation,None))
		return dict1
	

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
	else: 	
		result=[
			relateddict(dict(zip(columns, row)),change)
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
		if (name is None) or (short_name is None) or (user is None):
			response={"code":2,"response":"Invalid request"}
			return HttpResponse(dumps(response))
		else:

			new_forum=connection.cursor()
			new_forum.execute("insert into FORUM(name,short_name,user) values("+name+","+short_name+","+user+")")
			new_forum.execute("select ID as id,name,short_name,user from FORUM where name like %s and short_name like %s and user like %s",[name,short_name,user])
			response=dictfetchall(new_forum, None)
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
		details.execute('select ID as id, name, short_name, user from FORUM where short_name like %s group by short_name',[short_name])
		response=dictfetchall(details, None)
		if dumps(response)==[] is None:
			response1={"code":0,"response":"forum "+short_name+" does not exist"}
		else:
			response1={"code":0, "response":response}
		return HttpResponse(dumps(response1))
	else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))

       
def forumlistposts(request):
	if request.method == "GET":
		forum=request.GET.get("forum")
		since=request.GET.get("since")
		order=request.GET.get("order")
		related=request.GET.get("related")
		limit=request.GET.get("limit")
		if forum is None:
			response={"code":2,"response":"Invalid request, forum name required"}
			return HttpResponse(dumps(response))
		else:
			posts=connection.cursor()
			if order is None:
				order="desc"
			limiting=""
			if limit is not None:
				limiting=" LIMIT "+limit
			new_posts=""
			if since is not None:
				new_posts=" and date>="+since
			posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where forum=%s"+newposts+limitimg+"order by date "+order,[forum])
			response=dictfetchall(posts, related)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
		
	
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def forumlistthreads(request):
	if request.method == "GET":
		forum=request.GET.get("forum")
		since=request.GET.get("since")
		order=request.GET.get("order")
		related=request.GET.get("related")
		limit=request.GET.get("limit")
		if forum is None:
			response={"code":2,"response":"Invalid request, forum name required"}
			return HttpResponse(dumps(response))
		else:
			threads=connection.cursor()
			if order is None:
				order="desc"
			limiting=""
			if limit is not None:
				limiting=" LIMIT "+limit
			new_threads=""
			if since is not None:
				new_posts=" and date>="+since
			posts.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID ad id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select count(*) from POST where thread=THREAD.ID) as posts slug, title, user from THREAD where forum=%s"+newposts+limitimg+"order by date "+order,[forum])
			response=dictfetchall(posts, related)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
		
	
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def forumlistusers(request):
	if request.method == "GET":
		forum=request.GET.get("forum")
		since=request.GET.get("since_id")
		order=request.GET.get("order")
		limit=request.GET.get("limit")
		if forum is None:
			response={"code":2,"response":"Invalid request, forum name required"}
			return HttpResponse(dumps(response))
		else:
			users=connection.cursor()
			limiting=""
			if limit is not None:
				limiting=" LIMIT "+limit
			num=""
			if limit is not None:
				num=" LIMIT "+limit
			if order is None:
				order="desc"
			users.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER, POST where POST.forum=%s and POST.user=USER.email"+num+" order by name "+order, [forum])
			response=dictfetchall(users,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def postcreate(request):
	
	if request.method == "POST":
		date=request.POST.get("date")
		thread=request.POST.get("thread")
		message=request.POST.get("message")
		user=request.POST.get("user")
		forum=request.POST.get("forum")
		parent=request.POST.get("parent")
		if parent is None:
			parent="null"
		isApproved=request.POST.get("isApproved")
		if isApproved is None:
			isApproved="false"
		isHighlighted=request.POST.get("isHighlighted")
		if isHighlighted is None:
			isHighlighted="false"
		isEdited=request.POST.get("isEdited")
		if isEdited is None:
			isEdited="false"
		isSpam=request.POST.get("isSpam")
		if isSpam is None:
			isSpam="false"
		isDeleted=request.POST.get("isDeleted")
		if isDeleted is None:
			isDeleted="false"
		if (date is None) or (thread is None) or (message is None) or (user is None) or (forum is None):
			response={"code":2,"response":"Invalid request, forum, date, thread,message, user required"}
			return HttpResponse(dumps(response))
		else:
			post=connection.cursor()
			post.execute("insert into POST(date, thread, message, user, forum, parent, isApproved, isHighlighted, isEdited, isSpam, isDeleted) values("+date+","+thread+", %s,%s,%s, "+parent+", "+isApproved+", "+isHighlighted+", "+isEdited+", "+isSpam+", "+isDeleted+")", [message,user,forum])
			post.execute("select date, forum, ID as id, isApproved, isDeleted, isEdited, isHightlighted, isSpam,message,thread,user from POST where message like %s and user like %s and forum like %s and thread="+thread, [message,user, forum])
			response=dectfecthall(post, None)
			response1={"code":0, "response":response}
			return HttpResponse(dumps(response1))
				
	
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def postdetails(request):
	
	if request.method == "GET":
		post=request.GET.get("post")
		related=request.GET.get("related")
		if post is None:
			response={"code":2,"response":"Invalid request, post_id required"}
			return HttpResponse(dumps(response))
		else:
			post=connection.cursor()
			post.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from THREAD where ID="+post)
			response=dictfetchall(post, related)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def postlist(request):
	if request.method == "GET":
		forum=request.GET.get("forum")
		since=request.GET.get("since_id")
		order=request.GET.get("order")
		limit=request.GET.get("limit")
		thread=request.GET.get("thread")
		new_posts=""
		if since is not None:
			new_posts=" and date>="+date
		if order is None:
			order="desc"
		limiting=""
		if limit is not None:
			limitimg=" LIMIT "+limit
		if forum is not None:
			posts=connectiom.cursor()
			posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where forum=%s"+new_posts+limiting+"order by date "+order,[forum])
			response=dictfetchall(posts,None)
			response1={"code":0,"response":response}
			return HttpResponcse(dump(response1))
		else:
			if thread is not None:
				posts=connectiom.cursor()
				posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where thread="+thread+new_posts+limiting+"order by date "+order)
				response=dictfetchall(posts,None)
				response1={"code":0,"response":response}
				return HttpResponcse(dump(response1))
			else:
				response={"code":2,"response":"Invalid request, thread_id or forum name required"}
				return HttpResponse(dumps(response))

        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def postremove(request):
	
	if request.method=="POST":
		post=request.POST.get("post")
		if post is None:
			response={"code":2,"response":"Invalid request, post id required"}
			return HttpResponse(dumps(response))
		else:
			delete=connection.cursor()
			delete.execute("update POST set isDeleted=true where ID="+post)
			response={"code":0,"response":{"post", post"}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def postrestore(request):
	
	if request.method=="POST":
		post=request.POST.get("post")
		if post is None:
			response={"code":2,"response":"Invalid request, post id required"}
			return HttpResponse(dumps(response))
		else:
			delete=connection.cursor()
			delete.execute("update POST set isDeleted=false where ID="+post)
			response={"code":0,"response":{"post", post"}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def postupdate(request):

        if request.method=="POST":
		post=request.POST.get("post")
		message=request.POST.get("message")
		if (post is None) or (message is None):
			response={"code":2,"response":"Invalid request, post id required"}
			return HttpResponse(dumps(response))
		else:
			update=connection.cursor()
			update.execute("update POST set message=%s where ID="+post,[message])
			update.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where ID="+post)
			response=dictfetchall(update,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
		
def postvote(request):

        if request.method=="POST":
		post=request.POST.get("post")
		vote=request.POST.get("vote")
		if (post is None) or (vote is None):
			response={"code":2,"response":"Invalid request, post id and mark required"}
			return HttpResponse(dumps(response))
		else:
			vote=connection.cursor()
			vote.execute("insert into VOTE1(object,mark) values("+post+","+vote+")")
			vote.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where ID="+post)
			response=dictfetchall(vote,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

def usercreate(request):
	
	if request.method=="POST":
		isAnonymous=request.POST.get("isAnonymous")
		username=request.POST.get("username")
		about=request.POST.get("about")
		name=request.POST.get("name")
		email=request.POST.get("email")
		if isAnonymous is None:
			isAnonymous=" false"
		if (username is None) or (about is None) or (name is None) or (email is None):
			response={"code":2,"response":"Invalid request, name, username, email and about required"}
			return HttpResponse(dumps(response))
		else:
			newuser=connection.cursor()
			newuser.execute("insert into USER(username, name, about, email, isAnonymous) values(%s,%s,%s,%s,"+isAnonymous+")",[username,name,about,email])
			newuser.execute("select about,email, ID as id, isAnonymous,name,username from USER where email=%s",[email])
			response=dictfetchall(newuser,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
			
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

def userdetails(request):
		if request.method=="GET":
		email=request.GET.get("email")
		if email is None:
			response={"code":2,"response":"Invalid email required"}
			return HttpResponse(dumps(response))
		else:
			user=connection.cursor()
			user.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER, where email=%s", email)
			response=dictfetchall(user,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
			
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
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

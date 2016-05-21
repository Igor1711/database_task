#encoding:utf-8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection, transaction
from django.core.serializers import serialize
from json import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
import datetime			
			
def getobjectlist(cursor):
	columns=[col[0] for col in cursor.description]
	return [
		dict(zip(columns, row)).get("object")
		for row in cursor.fetchall()
	]

	
def changedictuser(user):
	user1=user
	follow=connection.cursor()
	follow.execute("select followee as object from FOLLOWING where follower like %s",[user1.get("email")])
	user1["following"]=getobjectlist(follow)
	follow.execute("select follower as object from FOLLOWING where followee like %s",[user1.get("email")])
	user1["followers"]=getobjectlist(follow)
	follow.execute("select threadid as object from SUBSCRIPTION where user like %s",[user1.get("email")])
	user1["subscriptions"]=getobjectlist(follow)
	return user1
	
def relateddict(dict1, relate):
	if relate is None:
		return dict1
	else: 
		forum=False
		user1=False
		thread=False
		for element in relate:
			if element=="forum":
				forum=True
			if element=="user":
				user1=True
			if element=="thread":
				thread=True
		if forum or user1 or thread:
			relation=connection.cursor()
			if forum:
				relation.execute("select ID as id, name,short_name,user from FORUM where short_name=%s",[dict1['forum']])
				dict1['forum']=dictfetchone(relation,None)
			if user1:
				relation.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER where email=%s", [dict1['user']])
				dict1['user']=dictfetchone(relation,"user")
			if thread:
				relation.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID as id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select(likes-dislikes)) as points, (select count(*) from POST where thread=THREAD.ID and isDeleted=0) as posts, slug, title, user from THREAD where ID="+str(dict1['thread']))
				dict1['thread']=dictfetchone(relation,None)
		return dict1
	

def dictfetchall(cursor, change):
	columns=[col[0] for col in cursor.description]
	if change is None:
		result= [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]
	else:
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
	
def dictfetchone(cursor, change):
	columns=[col[0] for col in cursor.description]
	if change is None:
		return dict(zip(columns, cursor.fetchone()))

	else:
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
        	return result[0]
def create_path(id, parent):
	if parent is None or parent=="null":
		return str(id)
	else:
		level=connection.cursor()
		level.execute("select parent from POST where id="+str(parent))
		num=dumps(level.fetchone()[0])
		
		return create_path(parent, num)+"."+str(id)
		
def tree(cursor, limit, date, order,thread):
	if order is None:
		order="desc"
	
	cursor.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where thread="+str(thread)+" and date>=cast(%s as datetime) and parent is null order by date "+order, [date])
	result=dictfetchall(cursor,None)
	relating=[]
	for post in result:
		relating.append(post)
		path=str(post.get("id"))+".%"
		cursor.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where thread="+str(thread)+" and date>=cast(%s as datetime) and path like %s order by path", [date, path])
		answers=dictfetchall(cursor,None)
		relating=relating+answers
	if limit is None or int(limit)>=len(relating):
		return relating
	else:

		res=[]
		i=0
		while i<int(limit):
			res.append(relating[i])
			i=i+1
		return res


def parent_tree(cursor, limit, date, order,thread):
	limiting=""
	if limit is not None:
		limiting =" LIMIT "+str(limit)
	if order is None:
		order="desc"
	cursor.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where thread="+str(thread)+" and date>=cast(%s as datetime) and parent is null order by date "+order+limiting, [date])
	result=dictfetchall(cursor,None)
	relating=[]
	for post in result:
		relating.append(post)
		path=str(post.get("id"))+".%"
		cursor.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where thread="+str(thread)+" and parent and path like %s order by path", [path])
		answers=dictfetchall(cursor,None)
		relating=relating+answers
	return relating 
		
@csrf_exempt
def clear(request):

	if request.method == "POST":
		forum=connection.cursor()
		forum.execute("DELETE from FORUM")
		forum.execute("delete from POST")
		forum.execute("delete from USER")
		forum.execute("delete from THREAD")
		forum.execute("delete from VOTE")
		forum.execute("delete from VOTE1")
		forum.execute("delete from SUBSCRIPTION")
		forum.execute("delete from FOLLOWING")
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
		numbers.execute("select (select count(*) from FORUM) as forum,(select count(*) from USER) as user, (select count(*) from THREAD) as thread, (select count(*) from POST) as post")
		response=dictfetchone(numbers,None)
		response1= {
			"code":0,
			"response":response
		}
		return HttpResponse(dumps(response1))
	else:
		response1={
			"code":3,
			"response":"error GET method required"
		}
		return HttpResponse(dumps(response1))
@csrf_exempt
def forumcreate(request):

	if request.method == "POST":
		data=loads(request.body)
		name=data.get("name")
		short_name=data.get("short_name")
		user=data.get("user")
		if name is None or short_name is None or user is None:
			response={"code":2,"response":"Invalid request"}
			return HttpResponse(dumps(response))
		else:
			code =0
			new_forum=connection.cursor()
			try:
				new_forum.execute("insert into FORUM(name,short_name,user) values(%s,%s,%s)",[name,short_name,user])
				new_forum.execute("select ID as id,name,short_name,user from FORUM where name like %s and short_name like %s and user like %s",[name,short_name,user])
				response=dictfetchone(new_forum, None)
			except Exception:
				response="Invalid data"
				new_forum.execute("delete from FORUM where short_name=%s",[short_name])
				code=3
			response1={"code":code,"response":response}
			return HttpResponse(dumps(response1))
	else:
		response={"code":3,"response":"error POST method required"}
		return HttpResponse(dumps(response))

def forumdetails(request):
	if request.method == "GET":
		short_name=request.GET.get("forum")
		related=[request.GET.get("related")]
		if short_name is None:
			response={"code":2,"response":"Invalid request, forum name required"}
			return HttpResponse(dumps(response))
		details=connection.cursor()
		related=['user']
		code=0
		details.execute('select ID as id, name, short_name, user from FORUM where short_name like %s group by short_name',[short_name])
		try:
			response=dictfetchone(details, None)
		except Exception:
			response="forum "+short_name+" does not exist"
			code=1
		response1={"code":code, "response":response}
		return HttpResponse(dumps(response1))
	else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))

       
def forumlistposts(request):
	if request.method == "GET":
		forum=request.GET.get("forum")
		since=request.GET.get("since")
		order=request.GET.get("order")
		related=[request.GET.get("related")]
		related=['forum','user','thread']
		limit=request.GET.get("limit")
		if forum is None:
			response={"code":2,"response":"Invalid request, forum name required"}
			return HttpResponse(dumps(response))
		else:
			posts=connection.cursor()
			if order is None:
				order="desc"
			limiting=" "
			if limit is not None:
				limiting=" LIMIT "+str(limit)
			if since is None:
				since='0000-00-00 00:00:00'
			posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where forum=%s and date>=date(cast(%s as datetime)) order by date "+order+limiting,[forum,since])
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
		related=[request.GET.get("related")]
		related=['forum','user']
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
				limiting=" LIMIT "+str(limit)
			new_threads=""
			if since is None:
				since="0000-00-00 00:00:00"
			threads.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID as id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message,(select(likes-dislikes)) as points, (select count(*) from POST where thread=THREAD.ID and isDeleted=0) as posts, slug, title, user from THREAD where forum=%s and date>=cast(%s as datetime) order by date "+order+limiting,[forum, since])
			response=dictfetchall(threads, related)
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
			num=""
			if limit is not None:
				num=" LIMIT "+str(limit)
			if order is None:
				order="desc"
			since_id=""
			if since is not None:
				since_id=" and USER.ID>="+str(since)
			users.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER, POST where POST.forum=%s and POST.user=USER.email GROUP by email order by name "+order+num, [forum])
			response=dictfetchall(users,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def postcreate(request):
	
	if request.method == "POST":
		data=loads(request.body)
		date=data.get("date")
		thread=data.get("thread")
		message=data.get("message")
		user=data.get("user")
		forum=data.get("forum")
		parent=data.get("parent")
		if parent is None:
			parent="null"
		isApproved=data.get("isApproved")
		if isApproved is None:
			isApproved="False"
		isHighlighted=data.get("isHighlighted")
		if isHighlighted is None:
			isHighlighted="False"
		isEdited=data.get("isEdited")
		if isEdited is None:
			isEdited="False"
		isSpam=data.get("isSpam")
		if isSpam is None:
			isSpam="False"
		isDeleted=data.get("isDeleted")
		if isDeleted is None:
			isDeleted="False"
		if date is None or thread is None or message is None or user is None or forum is None:
			response={"code":2,"response":"Invalid request, forum, date, thread,message, user required"}
			return HttpResponse(dumps(response))
		else:
			post=connection.cursor()
			code=0
			try:
				post.execute("insert into POST(date, thread, message, user, forum, parent, isApproved, isHighlighted, isEdited, isSpam, isDeleted) values(%s,"+str(thread)+", %s,%s,%s, "+str(parent)+", "+str(isApproved)+", "+str(isHighlighted)+", "+str(isEdited)+", "+str(isSpam)+", "+str(isDeleted)+")", [date,message,user,forum])
				post.execute("select date, forum, ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,message,thread,user from POST where message like %s and user like %s and forum like %s and thread="+str(thread), [message,user, forum])
				response=dictfetchone(post, None)
				post.execute("update POST set path=%s where ID="+str(response["id"]),[create_path(response["id"],parent)])
			except Exception:
				code=3
				response="Invalid data"
			response1={"code":code, "response":response}
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
			posts=connection.cursor()
			code=0
			try:
				posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT (likes-dislikes)) as points, thread, user from POST where ID= "+str(post))
				response=dictfetchone(posts, related)
			except Exception:
				code=1
				response="404 post not found"
			response1={"code":code,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def postlist(request):
	if request.method == "GET":
		forum=request.GET.get("forum")
		since=request.GET.get("since")
		order=request.GET.get("order")
		limit=request.GET.get("limit")
		thread=request.GET.get("thread")
		if since is None:
			since="0000-00-00 00:00:00"
		if order is None:
			order="desc"
		limiting=""
		if limit is not None:
			limiting=" LIMIT "+str(limit)
		if forum is not None:
			posts=connection.cursor()
			posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where forum=%s and date>=cast(%s as datetime) order by date "+order+limiting,[forum,since])
			response=dictfetchall(posts,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
		else:
			if thread is not None:
				posts=connection.cursor()
				posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where thread="+str(thread)+" and date>=cast(%s as datetime) order by date "+order+limiting,[since])
				response=dictfetchall(posts,None)
				response1={"code":0,"response":response}
				return HttpResponse(dumps(response1))
			else:
				response={"code":2,"response":"Invalid request, thread_id or forum name required"}
				return HttpResponse(dumps(response))

        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def postremove(request):
	
	if request.method=="POST":
		data=loads(request.body)
		post=data.get("post")
		if post is None:
			response={"code":2,"response":"Invalid request, post id required"}
			return HttpResponse(dumps(response))
		else:
			delete=connection.cursor()
			delete.execute("update POST set isDeleted=true where ID="+str(post))
			response={"code":0,"response":{"post": post}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def postrestore(request):
	
	if request.method=="POST":
		data=loads(request.body)
		post=data.get("post")
		if post is None:
			response={"code":2,"response":"Invalid request, post id required"}
			return HttpResponse(dumps(response))
		else:
			delete=connection.cursor()
			delete.execute("update POST set isDeleted=false where ID="+str(post))
			response={"code":0,"response":{"post": post}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def postupdate(request):

        if request.method=="POST":
		data=loads(request.body)
		post=data.get("post")
		message=data.get("message")
		if (post is None) or (message is None):
			response={"code":2,"response":"Invalid request, post id required"}
			return HttpResponse(dumps(response))
		else:
			update=connection.cursor()
			update.execute("update POST set message=%s where ID="+str(post),[message])
			update.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where ID="+str(post))
			response=dictfetchone(update,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
		
def postvote(request):

        if request.method=="POST":
		data=loads(request.body)
		post=data.get("post")
		vote1=data.get("vote")
		if (post is None) or (vote1 is None):
			response={"code":2,"response":"Invalid request, post id and mark required"}
			return HttpResponse(dumps(response))
		else:
			vote=connection.cursor()
			vote.execute("insert into VOTE1(object,mark) values("+str(post)+","+str(vote1)+")")
			vote.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where ID="+str(post))
			response=dictfetchone(vote,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
@csrf_exempt
def usercreate(request):
	
	if request.method=="POST":
		data=loads(request.body)
		isAnonymous=str(data.get("isAnonymous"))
		username=data.get("username")
		about=data.get("about")
		name=data.get("name")
		email=data.get("email")
		if isAnonymous is None:
			isAnonymous="False"
		if email is None:
			response={"code":2,"response":"Invalid request, name, username, email and about required"}
			return HttpResponse(dumps(response))
		else:
			newuser=connection.cursor()
			code=0
			try:
				newuser.execute("insert into USER(username, name, about, email, isAnonymous) values(%s,%s,%s,%s,"+isAnonymous+")",[username,name,about,email])
				newuser.execute("select about,email, ID as id, isAnonymous,name,username from USER where email=%s",[email])
				response=dictfetchone(newuser,None)
			except Exception:
				code=5
				response="such user already exists"
			response1={"code":code,"response":response}
			return HttpResponse(dumps(response1))
			
        else:
		 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

def userdetails(request):
	if request.method=="GET":
		email=request.GET.get("user")
		if email is None:
			response={"code":2,"response":"Invalid email required"}
			return HttpResponse(dumps(response))
		else:
			user=connection.cursor()
			code=0
			try:
				user.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER where email like %s", [email])
				response=dictfetchone(user,"user")
			except Exception:
				code=1
				response="404 user not found"
			response1={"code":code,"response":response}
			return HttpResponse(dumps(response1))
			
	else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
		
def userfollow(request):
	
	if request.method=="POST":
		data=loads(request.body)
		follower=data.get("follower")
		followee=data.get("followee")
		if (follower is None or followee is None):
			response={"code":2,"response":"Invalid request, follower and followee required"}
			return HttpResponse(dumps(response))
		else:
			follow=connection.cursor()
			follow.execute("insert FOLLOWING(follower,followee) values(%s,%s)",[follower,followee])
			follow.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER where email like %s", [follower])
			response=dictfetchone(follow,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
			
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

def userlistfollowers(request):
	
	if request.method=="GET":
		user=request.GET.get("user")
		if user is None:
			response={"code":2,"response":"Invalid request, user required"}
			return HttpResponse(dumps(response))
		else:
			order=request.GET.get("order")
			if order is None:
				order="desc"
			limit=request.GET.get("limit")
			limiting=""
			if limit is not None:
				limiting=" LIMIT "+str(limit)
			since=request.GET.get("since_id")
			news=""
			if since is not None:
				news="and ID>="+str(since)
			followers=connection.cursor()
			followers.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER where email in (select follower from FOLLOWING where followee like %s "+news+") order by name "+order+limiting, [user])
			response=dictfetchall(followers,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))

        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))

def userlistfollowing(request):

        if request.method=="GET":
		user=request.GET.get("user")
		if user is None:
			response={"code":2,"response":"Invalid request, user required"}
			return HttpResponse(dumps(response))
		else:
			order=request.GET.get("order")
			if order is None:
				order="desc"
			limit=request.GET.get("limit")
			limiting=""
			if limit is not None:
				limiting=" LIMIT "+str(limit)
			since=request.GET.get("since_id")
			news=""
			if since is not None:
				news="and ID>="+str(since)
			followers=connection.cursor()
			followers.execute("select about, email, email as following,email as followers, USER.ID as id, isAnonymous,name, email as subscriptions, username from USER where email in (select followee from FOLLOWING where follower like %s "+news+") order by name "+order+limiting , [user])
			response=dictfetchall(followers,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
		
        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))


def userlistposts(request):

        if request.method=="GET":
		user=request.GET.get("user")
		if user is None:
			response={"code":2,"response":"Invalid request, user required"}
			return HttpResponse(dumps(response))
		else:
			order=request.GET.get("order")
			if order is None:
				order="desc"
			limit=request.GET.get("limit")
			limiting=""
			if limit is not None:
				limiting=" LIMIT "+str(limit)
			since=request.GET.get("since")
			buff="'"
			if since is not None:
				since="0000-00-00 00:00:00"
			posts=connection.cursor()
			posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where user like %s order by date "+order+limiting,[user])
			response=dictfetchall(posts,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))

        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))


def userunfollow(request):

       	if request.method=="POST":
		data=loads(request.body)
		follower=data.get("follower")
		followee=data.get("followee")
		if (follower is None or followee is None):
			response={"code":2,"response":"Invalid request, follower and followee required"}
			return HttpResponse(dumps(response))
		else:
			follow=connection.cursor()
			follow.execute("delete from FOLLOWING where follower like %s and followee like %s",[follower,followee])
			follow.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER where email like %s", [follower])
			response=dictfetchone(follow,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
			
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

def userupdateprofile(request):
	
	if request.method=="POST":
		data=loads(request.body)
		user=data.get("user")
		about=data.get("about")
		name=data.get("name")
		if (user is None or about is None or name is None):
			response={"code":2,"response":"Invalid request, user email about and name required"}
			return HttpResponse(dumps(response))
		else:
			update=connection.cursor()
			update.execute("update USER set name=%s, about=%s where email like %s", [name, about, user])
			update.execute("select about, email, email as following, email as followers, USER.ID as id, isAnonymous, name, email as subscriptions, username from USER where email like %s", [user])
			response=dictfetchall(update,"user")
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
	
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

def threadclose(request):

        if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		if thread is None:
			response={"code":2,"response":"Invalid request, thread id required"}
			return HttpResponse(dumps(response))
		else:
			close=connection.cursor()
			close.execute("update THREAD set isClosed=True where ID="+str(thread))
			response={"code":0,"response":{"thread":thread}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

def threadcreate(request):
	
	if request.method=="POST":
		data=loads(request.body)
		isDeleted=data.get("isDeleted")
		if isDeleted is None:
			isDeleted="false"
		forum=data.get("forum")
		title=data.get("title")
		isClosed=data.get("isClosed")
		user=data.get("user")
		date=data.get("date")
		message=data.get("message")
		slug=data.get("slug")
		if (forum is None or title is None or isClosed is None or user is None or date is None or message is None or slug is None):
			response={"code":2,"response":"Invalid request, fill all fields required"}
			return HttpResponse(dumps(response))
		else:
			newthread=connection.cursor()
			newthread.execute("insert into THREAD(forum, title, isClosed, user, date, message,slug, isDeleted) values(%s,%s,"+str(isClosed)+",%s,%s,%s,%s,"+str(isDeleted)+")",[forum,title,user,date,message,slug])
			newthread.execute("select date,forum,ID as id,isClosed, isDeleted,message,slug,title,user from THREAD where forum like %s and title like %s and user like %s and message like %s",[forum,title,user,message])
			response=dictfetchone(newthread,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
	
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

        
def threaddetails(request):
	
	if request.method=="GET":
		related=request.GET.get("related")
		thread=request.GET.get("thread")
		if related=="thread":
			response={"code":3,"response":"invalid related"}
                        return HttpResponse(dumps(response))
		related=[request.GET.get("thread")]

		if thread is None:
			response={"code":2,"response":"Invalid request, thread id required"}
			return HttpResponse(dumps(response))
		else:
			detail=connection.cursor()
			code=0
			try:
				detail.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID as id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select(likes-dislikes)) as points, (select count(*) from POST where thread=THREAD.ID and isDeleted=0) as posts, slug, title, user from THREAD where ID="+str(thread))
				response=dictfetchone(detail,related)
			except Exception:
				code=1
				response="404 thread not found"
			response1={"code":code,"response":response}
			return HttpResponse(dumps(response1))

        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))

def threadlist(request):

	if request.method=="GET":
		forum=request.GET.get("forum")
		since=request.GET.get("since")
		order=request.GET.get("order")
		limit=request.GET.get("limit")
		user=request.GET.get("user")
		if since is None:
			since="0000-00-00 00:00:00"
		if order is None:
			order="desc"
		limiting=""
		if limit is not None:
			limiting=" LIMIT "+str(limit)
		if forum is not None:
			threads=connection.cursor()
			threads.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID as id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select(likes-dislikes)) as points, (select count(*) from POST where thread=THREAD.ID) as posts, slug, title, user from THREAD where forum like %s and date>=cast(%s as datetime) order by date "+order+ limiting,[forum,since])
			response=dictfetchall(threads,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
		else:
			if user is not None:
				threads=connection.cursor()
				threads.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID as id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select(likes-dislikes)) as points, (select count(*) from POST where thread=THREAD.ID) as posts, slug, title, user from THREAD where user like %s and date>=cast(%s as datetime) order by date "+order+limiting,[user,since])
				response=dictfetchall(threads,None)
				response1={"code":0,"response":response}
				return HttpResponse(dumps(response1))
			else:
				response={"code":2,"response":"Invalid request, thread_id or forum name required"}
				return HttpResponse(dumps(response))

        else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))

def threadlistposts(request):

        if request.method=="GET":
		
		since=request.GET.get("since")
		order=request.GET.get("order")
		limit=request.GET.get("limit")
		thread=request.GET.get("thread")
		sort=request.GET.get("sort")
		if since is None:
			since="0000-00-00 00:00:00"
		if order is None:
			order="desc"
		if sort is None:
			sort="flat"
		limiting=""
                if limit is not None:
                        limiting=" LIMIT "+str(limit)
		if thread is None:
			response={"code":2,"response":"Invalid request, thread_id required"}
			return HttpResponse(dumps(response))
		else:
			posts=connection.cursor()
			if sort=="flat":
				posts.execute("select date, (select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=-1) as dislikes, forum,ID as id, isApproved, isDeleted, isEdited, isHighlighted, isSpam,(select count(*) from VOTE1 where VOTE1.object=POST.ID and mark=1) as likes, message, parent, (SELECT likes-dislikes) as points, thread, user from POST where thread="+str(thread)+" and date>=cast(%s as datetime) order by date "+order+limiting, [since])
				response=dictfetchall(posts,None)
			else:
				if sort=="tree":
					response=tree(posts,limit,since,order,thread)
				else:
					response=parent_tree(posts,limit,since,order,thread)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
			
	else: 
		response={"code":3, "response":"error expected GET request"}
		return HttpResponse(dumps(response))
        
def threadopen(request):

        if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		if thread is None:
			response={"code":2,"response":"Invalid request, thread id required"}
			return HttpResponse(dumps(response))
		else:
			open1=connection.cursor()
			open1.execute("update THREAD set isClosed=False where ID="+str(thread))
			response={"code":0,"response":{"thread": thread}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def threadremove(request):

        if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		if thread is None:
			response={"code":2,"response":"Invalid request, thread id required"}
			return HttpResponse(dumps(response))
		else:
			close=connection.cursor()
			close.execute("update THREAD set isDeleted=true where ID="+str(thread))
			close.execute("update POST set isDeleted=true where thread="+str(thread))
			response={"code":0,"response":{"thread": thread}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def threadrestore(request):

        if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		if thread is None:
			response={"code":2,"response":"Invalid request, thread id required"}
			return HttpResponse(dumps(response))
		else:
			close=connection.cursor()
			close.execute("update THREAD set isDeleted=False where ID="+str(thread))
			close.execute("update POST set isDeleted=False where thread="+str(thread))
			response={"code":0,"response":{"thread": thread}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
		
def threadsubscribe(request):
	
	if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		user=data.get("user")
		if (user is None or thread is None):
			response={"code":2,"response":"Invalid request, thread id and username required"}
			return HttpResponse(dumps(response))
		else:
			sudscribe=connection.cursor()
			sudscribe.execute("insert into SUBSCRIPTION(threadid,user) values("+str(thread)+",%s)",[user])
			response={"code":0,"response":{"thread": thread, "user": user}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))

        
def threadunsubscribe(request):

       	if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		user=data.get("user")
		if (user is None or thread is None):
			response={"code":2,"response":"Invalid request, thread id and username required"}
			return HttpResponse(dumps(response))
		else:
			sudscribe=connection.cursor()
			sudscribe.execute("delete from SUBSCRIPTION where threadid="+str(thread)+" and user like %s",[user])
			response={"code":0,"response":{"thread": thread, "user": user}}
			return HttpResponse(dumps(response))
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
        
def threadupdate(request):

        if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		message=data.get("message")
		slug=data.get("slug")
		if (thread is None or message is None or slug is None):
			response={"code":2,"response":"Invalid request, user email about and name required"}
			return HttpResponse(dumps(response))
		else:
			update=connection.cursor()
			update.execute("update THREAD set slug=%s, message=%s where ID="+str(thread), [slug, message])
			update.execute("select date, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID as id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select(likes-dislikes)) as points, (select count(*) from POST where thread=THREAD.ID) as posts, slug, title, user from THREAD where ID="+str(thread))
			response="dictfetchone(update,None)"
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
	
        else: 
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))
def threadvote(request):

	if request.method=="POST":
		data=loads(request.body)
		thread=data.get("thread")
		vote1=data.get("vote")
		if (thread is None or vote1 is None):
			response={"code":2,"response":"Invalid request, post id and mark required"}
			return HttpResponse(dumps(response))
		else:
			vote=connection.cursor()
			vote.execute("insert into VOTE(object,mark) values("+str(thread)+","+str(vote1)+")")
			vote.execute("select date,(select count(*) from VOTE where VOTE.object=THREAD.ID and mark=-1) as dislikes, forum, ID as id, isClosed, isDeleted, (select count(*) from VOTE where VOTE.object=THREAD.ID and mark=1) as likes, message, (select(likes-dislikes)) as points, (select count(*) from POST where thread=THREAD.ID) as posts, slug, title, user from THREAD where ID="+str(thread))
			response=dictfetchone(vote,None)
			response1={"code":0,"response":response}
			return HttpResponse(dumps(response1))
	else:
		response={"code":3, "response":"error expected POST request"}
		return HttpResponse(dumps(response))




# Create your views here.

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User

from sae.storage import Bucket, Client
from sae.ext.storage import monkey
monkey.patch_all()

from datetime import *
from markdown import markdown
from random import randint

# Create your views here.

def get_last_event():
	last_event = Event.objects.order_by('-event_time')
	if len(last_event) > 0:
		last_event = last_event[0]
	else:
		last_event = Event(id = 0)
	return last_event

def home(req):
	return render_to_response('index.html',{'last_event':get_last_event()})

def admin(req):
	if req.session.get('username',''):
		return render_to_response('panel.html',{})
	status = ''
	if req.POST:
		post = req.POST
		username = post['username']
		password = post['passwd']
		if User.objects.filter(username = username):
			user = auth.authenticate(username = username, password = password)
			if user is not None:
				if user.is_active:
					auth.login(req,user)
					req.session['username'] = username
					return render_to_response('panel.html',{})
				else:
					status = 'NOTACTIVE'
			else:
				status = 'PASSWDERR'
		else:
			status = "NOTEXIST"
	content = {'status':status,'last_event':get_last_event()}
	return render_to_response('login.html',content,context_instance = RequestContext(req))

def logout(req):
	auth.logout(req)
	return HttpResponseRedirect('/')

def addDynamics(req):
	username = req.session.get("username",'')
	if username == "":
		return HttpResponseRedirect("/")
	else:
		user = User.objects.get(username = username)
		if req.POST:
			post = req.POST
			new_dynamics = Dynamics(title = post['title'], \
									author = user, \
									content = post['content'], \
									model = post['model'], \
									)
			if post['hasform'] == "False":
				new_dynamics.hasform = False
			else:
				new_dynamics.hasform = True
			new_dynamics.save()
			if new_dynamics.hasform == True:
				new_evevt = Event(name = post['name'], \
									event_time = post['event_time'], \
									number = post['number'], \
									now_num = 0, \
									start_time = post['start_time'], \
									end_time = post['end_time'], \
									dynamics = new_dynamics, \
									)
				if ('needname' in post) and (post['needname'] == "True"):
					new_evevt.needname = True
				if ('needcollege' in post) and (post['needcollege'] == "True"):
					new_evevt.needcollege = True
				if ('needgrade' in post) and (post['needgrade'] == "True"):
					new_evevt.needgrade = True
				if ('needphone' in post) and (post['needphone'] == "True"):
					new_evevt.needphone = True
				if ('needemail' in post) and (post['needemail'] == "True"):
					new_evevt.needemail = True
				if ('needqq' in post) and (post['needqq'] == "True"):
					new_evevt.needqq = True
				if ('needothername' in post) and (post['needothername'] == "True"):
					new_evevt.needothername = True
					new_evevt.othername = post['othername']
				new_evevt.save()
				return HttpResponseRedirect('/dynlist')
		return render_to_response('addDynamics.html',{'last_event':get_last_event()},context_instance = RequestContext(req))

def dynlist(req):
	dynlst = Dynamics.objects.order_by('-publish_time')
	content = {"dynlst":dynlst,'last_event':get_last_event()}
	return render_to_response('dynlist.html', content)

def dyndetail(req):
	Id = req.GET['id']
	try:
		dyn = Dynamics.objects.get(pk = Id)
	except:
		return HttpResponseRedirect('/dynlist')
	if dyn.model == 2:
		dyn.content = markdown(dyn.content)
	content = {'dyn':dyn,'last_event':get_last_event()}
	return render_to_response('dyndetail.html',content)

def join(req):
	Id = req.GET['id']
	y = date.today().year
	year_list = [y - 3, y - 2, y - 1, y]
	try:
		event = Event.objects.get(pk = Id)
	except:
		return HttpResponseRedirect('/dynlist')
	if req.POST:
		state = ''
		dt = datetime.now()
		post = req.POST
		t = event.end_time
		if dt > datetime(t.year,t.month,t.day,t.hour,t.minute,t.second):
			state = "time_out"
			return render_to_response('reseult.html',{'state':state,'last_event':get_last_event()})
		elif event.now_num >= event.number:
			state = 'over_number'
			return render_to_response('reseult.html',{'state':state,'last_event':get_last_event()})
		else:
			partake = Partake(event = event)
			if 'name' in post:
				partake.name = post['name']
			if 'college' in post:
				partake.college = post['college']
			if 'grade' in post:
				partake.grade = post['grade']
			if 'phone' in post:
				partake.phone = post['phone']
			if 'email' in post:
				partake.email = post['email']
			if 'qq' in post:
				partake.qq = post['qq']
			if 'other' in post:
				partake.other = post['other']
			partake.save()
			event.now_num = event.now_num + 1
			event.save()
			state = 'success'
			return render_to_response('reseult.html',{'state':state,'last_event':get_last_event()})
	content = {'event':event,'year':year_list,'last_event':get_last_event()}
	return render_to_response('join.html',content,context_instance = RequestContext(req));

def eventlst(req):
	username = req.session.get("username",'')
	if username == '':
		return HttpResponseRedirect('/admin')
	else:
		eventlst = Event.objects.order_by('-event_time')
		content = {"eventlst":eventlst,'last_event':get_last_event()}
		return render_to_response('eventlst.html',content)

def eventdetail(req):
	username = req.session.get("username",'')
	if username == '':
		return HttpResponseRedirect('/admin')
	else:
		Id = req.GET['id']
		try:
			event = Event.objects.get(pk = Id)
		except:
			return HttpResponseRedirect('/eventlst')
		partakelst = Partake.objects.filter(event = event)
		content = {"event":event,"partakelst":partakelst,'last_event':get_last_event()}
		return render_to_response('eventdetail.html',content)

def imgupload(req):
	username = req.session.get("username",'')
	if username == '':
		return HttpResponseRedirect('/admin')
	else:
		if req.POST:
			post = req.POST
			if req.FILES:
				img = req.FILES['img']
				# s = Client()
				bucket = Bucket('img')
				# st = bucket.conn.__dict__
				# if bucket.stat()['bytes'] == '0':
				bucket.put()
				bucket.post(acl='.r:.sinaapp.com,.r:sae.sina.com.cn')
				tut = img._name.split('.')[-1]
				dt_str = datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')
				filename = dt_str + str(randint(100,999)) + '.' + tut
				bucket.put_object(filename,img)
				# s.put('hitmstcweb',filename,img)
				image = Img(
							name = post.get('name','dt_str'), \
							descripe = post.get('descripe',''), \
							img = bucket.generate_url(filename), \
							author = User.objects.get(username = username), \
							)
				image.save()
	content = {'last_event':get_last_event()}
	return render_to_response('imgupload.html',content,context_instance = RequestContext(req));

def imglist(req):
	username = req.session.get("username",'')
	if username == '':
		return HttpResponseRedirect('/admin')
	else:
		imglst = Img.objects.order_by('-uptime')
		content = {'imglst':imglst, 'last_event':get_last_event()}
		return render_to_response('imglist.html',content)
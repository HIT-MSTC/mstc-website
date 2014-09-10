from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User

from datetime import *

# Create your views here.
def home(req):
	return render_to_response('index.html',{})

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
	content = {'status':status}
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
		return render_to_response('addDynamics.html',{},context_instance = RequestContext(req))

def dynlist(req):
	dynlst = Dynamics.objects.order_by('-publish_time')
	content = {"dynlst":dynlst}
	return render_to_response('dynlist.html', content)

def dyndetail(req):
	Id = req.GET['id']
	try:
		dyn = Dynamics.objects.get(pk = Id)
	except:
		return HttpResponseRedirect('/dynlist')
	content = {'dyn':dyn}
	return render_to_response('dyndetail.html',content)

def join(req):
	Id = req.GET['id']
	y = date.today().year
	year_list = [y - 3, y - 2, y - 1, y]
	try:
		event = Event.objects.get(pk = Id)
	except:
		return HttpResponseRedirect('/dynlist/')
	if req.POST:
		state = ''
		dt = datetime.now()
		post = req.POST
		t = event.end_time
		if dt > datetime(t.year,t.month,t.day,t.hour,t.minute,t.second):
			stata = "time_out"
			return render_to_response('reseult.html',{'state':state})
		elif event.now_num >= event.number:
			state = 'over_number'
			return render_to_response('reseult.html',{'state':state})
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
			stata = 'success'
			return render_to_response('reseult.html',{'state':state})
	content = {'event':event,'year':year_list}
	return render_to_response('join.html',content,context_instance = RequestContext(req));
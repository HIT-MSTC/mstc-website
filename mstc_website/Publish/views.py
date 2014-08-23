from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def home(req):
	content = {'active_item':'homepage'}
	return render_to_response('index.html',content)
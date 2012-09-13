#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import cgi

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.template import Context,Template,loader
from django import forms

from google.appengine.ext import db


class avwork(db.Model):
    yourname = db.StringProperty()
    filesetname = db.StringProperty()
    submitdate = db.DateTimeProperty(auto_now=True)
    language = db.StringProperty()
    kav = db.StringProperty()
    nod32 = db.StringProperty()
    comment = db.StringProperty(multiline=True)
    status = db.StringProperty()
    hot=db.StringProperty()


class myForm(forms.Form):
    yourname=forms.CharField()
    filesetname=forms.CharField()
    CHOICE=(
	('none','none'),
	('VB','VB'),
	('VC','VC'),
	('DELPHI','DELPHI'),
	('dotNET','dotNET'),
	)
    HOT=(
	('normal','normal'),
	('redline','redline'),
	)
    language=forms.ChoiceField(CHOICE)
    kav=forms.CharField()
    nod32=forms.CharField()
    hot=forms.ChoiceField(widget=forms.RadioSelect,choices=HOT,initial='normal')
    status = forms.CharField()
    comment=forms.CharField(widget=forms.Textarea)


class MainHandler(webapp2.RequestHandler):
	def get(self):
		form=myForm()
		avworks = avwork.all()
		avworks.order('-submitdate')
		#avworks.filter('status !=','!')
		t=loader.get_template('index.html')
		c=Context({"my_name":"Fileset Board","avworks":avworks,'form':form})
		self.response.out.write(t.render(c))

class MainHandlerFilter(webapp2.RequestHandler):
    def get(self,filter):
		form=myForm()
		avworks = avwork.all()
		avworks.order('-submitdate')
		avworks.filter('status =',filter)
		t=loader.get_template('index.html')
		c=Context({"my_name":"Fileset Board","avworks":avworks,'form':form})
		self.response.out.write(t.render(c))

class MainHandlerSortbyb(webapp2.RequestHandler):
    def get(self):
	        form=myForm()
	        avworks = avwork.all()
	        avworks.order('-submitdate')
	        avworks.filter('status =','*')
	        t=loader.get_template('index.html')
	        c=Context({"my_name":"Fileset Board","avworks":avworks,'form':form})
	        self.response.out.write(t.render(c))


class SortHandler(webapp2.RequestHandler):
    def get(self,cols):
        form=myForm()
	avworks = avwork.all()
	avworks.order(cols)
	t=loader.get_template('index.html')
	c=Context({"my_name":"Fileset Board","avworks":avworks,'form':form})
	self.response.out.write(t.render(c))

class ProductHandler(webapp2.RequestHandler):
    def get (self,product_id):
	c=Context({"my_name":"zyguo"})
	t=loader.get_template('index.html')
	self.response.out.write(t.render(c))
	
class AddHandler(webapp2.RequestHandler):
    def post(self):
	self.response.out.write(cgi.escape(self.request.get('yourname')))
	yourname=self.request.get('yourname')
	work=avwork()
	work.yourname=self.request.get('yourname')
	work.filesetname=self.request.get('filesetname')
	work.language=self.request.get('language')
	work.nod32=self.request.get('nod32')
	work.kav=self.request.get('kav')
	work.comment=self.request.get('comment')
	work.status=self.request.get('status')
	work.hot=self.request.get('hot')
	work.put()
	self.redirect('/') 

class DeleteHandler(webapp2.RequestHandler):
    def get(self,id):
		w=avwork.get_by_id(int(id))
		w.delete()
		self.redirect('/')

		
class EditHandler(webapp2.RequestHandler):
    def get(self,id):
		w=avwork.get_by_id(int(id))
		data={
		'yourname':w.yourname,
		'filesetname':w.filesetname,
		'language':w.language,
		'nod32':w.nod32,
		'kav':w.kav,
		'comment':w.comment,
		'hot':w.hot,
		'status':w.status,
		}
		form=myForm(data)
		t=loader.get_template('edit.html')
		c=Context({"my_name":"Fileset Board",'form':form,'id':int(id)})
		self.response.out.write(t.render(c))

    def post(self,id):
		self.response.out.write('G!!!!!')
		work=avwork.get_by_id(int(id))
	   	work.yourname=self.request.get('yourname')
		work.filesetname=self.request.get('filesetname')
		work.language=self.request.get('language')
		work.nod32=self.request.get('nod32')
		work.kav=self.request.get('kav')
		work.comment=self.request.get('comment')
		work.status=self.request.get('status')
		work.hot=self.request.get('hot')
		work.put()
		self.redirect('/')

		


app = webapp2.WSGIApplication([
	(r'/', MainHandler),
	(r'/sort/(.*)', SortHandler),
	(r'/add', AddHandler),
	(r'/(\d+)',ProductHandler),
	(r'/delete/(\d+)', DeleteHandler),
	(r'/edit/(\d+)', EditHandler),
	(r'/filter/(.{1})',MainHandlerFilter),
	], debug=True)

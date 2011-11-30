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

import cgi
import datetime
import urllib
import wsgiref.handlers
import logging
import os

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AirNote(db.Model):
  geolocation = db.GeoPtProperty()
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def airnotebook_key(airnotebook_location=None):
  return db.Key.from_path('AirNotebook', airnotebook_location or 'default_location')


class MainPage(webapp.RequestHandler):
  def get(self):
  
    logging.info('Start MainPage')
    airnotebook_location=self.request.get('airnotebook_location')

    logging.info('Location: %s', airnotebook_location)
    
    airnotes = db.GqlQuery("SELECT * "
                            "FROM AirNote "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY date",
                            airnotebook_key(airnotebook_location))

    logging.info('Airnotes count: %s', airnotes.count())

    template_values = {
            'airnotes': airnotes,
            'geolocation': airnotebook_location,
    }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))


class AirNotebook(webapp.RequestHandler):
  def post(self):
    logging.info('Start AirNotebook')
    airnotebook_location = self.request.get('airnotebook_location')
    logging.info('Location: %s', airnotebook_location)
    airnote = AirNote(parent=airnotebook_key(airnotebook_location))	
    airnote.geolocation = airnotebook_location
    airnote.content = self.request.get('content')
    if users.get_current_user():
        airnote.author = users.get_current_user()
    airnote.put()
    self.redirect('/?' + urllib.urlencode({'airnotebook_location': airnotebook_location}))


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/note', AirNotebook)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

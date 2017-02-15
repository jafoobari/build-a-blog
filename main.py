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
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape= True)

class Posts(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add= True)


class MainHandler(webapp2.RequestHandler):
    def get(self, *a, **kw):
        posts = db.GqlQuery("SELECT * FROM Posts ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("frontpage.html")
        content = t.render(
            title = "",
            body = "",
            error = self.request.get("error"),
            posts = posts)
        self.response.write(content)

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            post = Posts(title = title, body = body)
            post.put()
        #put in a redirect to to the frontpage here
            #once this gets moved to the newpost handler
            confirmation = "Your post has been added to the blog. Add another!"
            self.redirect("/?error=" + confirmation)
        else:
            error = "Please insert both a title and body for your blog post."
            self.redirect("/?error=" + error)


#TODO: Handler for '/blog'.
# The /blog route displays the 5 most recent posts. To limit the displayed posts in this way, you'll need to filter the query results.

#TODO: Handler for '/newpost'
#After submitting a new post, your app displays the main blog page.
# Note that, as with the AsciiChan example, you will likely need to refresh the main blog page to see your new post listed.

#TODO: Check for blank title and/or body
# If either title or body is left empty in the new post form, the form is rendered again, with a helpful error message
# and any previously-entered content in the same form inputs.
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

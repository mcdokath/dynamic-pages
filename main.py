import webapp2

application = webapp2.WSGIApplication([
  ('/', 'base_page.DynamicPage'),
], debug=True)

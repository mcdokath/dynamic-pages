import webapp2

config = {'default-group':'base-data'}

application = webapp2.WSGIApplication([
  ('/', 'base_page.DynamicPage'),
], debug=True, config=config)
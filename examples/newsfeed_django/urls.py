import os
from django.conf.urls.defaults import *

from views import Home, Post

urlpatterns = patterns('',
    # as the docs say: "Do not use this in a production setting"
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static'),}),
    
    url(r'^post/', Post, name='post'),
    url(r'^$', Home, name='home'),
)

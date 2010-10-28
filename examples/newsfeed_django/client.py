#!/usr/bin/env python
#
# Copyright 2010 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A Facebook stream client written against the Facebook Graph API."""

import facebook

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import FacebookUser


class ClientViewHelper(object):
    def __init__(self, request):
        """
        The xxxHandler classes in the AppEngine example are something like
        class-based views in Django. But it's difficult to do class-based views
        in a thread-safe way, so it's cleaner and simpler just to instantiate
        this helper class from within regular views.
        """
        self.request = request
    
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_user(self):
        """Returns the active user, or None if the user has not logged in."""
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(
                self.request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
            if cookie:
                # Store a local instance of the user data so we don't need
                # a round-trip to Facebook on every request
                try:
                    user = FacebookUser.objects.get(uid=cookie["uid"])
                except FacebookUser.DoesNotExist:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = FacebookUser(pk=str(profile["id"]),
                                        name=profile["name"],
                                        profile_url=profile["link"],
                                        access_token=cookie["access_token"])
                    user.save()
                else:
                    if user.access_token != cookie["access_token"]:
                        user.access_token = cookie["access_token"]
                        user.save()
                self._current_user = user
        return self._current_user

    @property
    def graph(self):
        """Returns a Graph API client for the current user."""
        if not hasattr(self, "_graph"):
            if self.current_user:
                self._graph = facebook.GraphAPI(self.current_user.access_token)
            else:
                self._graph = facebook.GraphAPI()
        return self._graph

    def render(self, template, **kwargs):
        args = dict(current_user=self.current_user,
                    facebook_app_id=settings.FACEBOOK_APP_ID)
        args.update(kwargs)
        return render_to_response(template, args,
            context_instance=RequestContext(self.request)
        )



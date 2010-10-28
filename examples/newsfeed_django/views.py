import datetime
import facebook

from django.shortcuts import redirect

from client import ClientViewHelper


def Home(request):
    client = ClientViewHelper(request)
    if not client.current_user:
        return client.render("newsfeed_django/index.html")
    try:
        news_feed = client.graph.get_connections("me", "home")
    except facebook.GraphAPIError as err:
        return client.render("newsfeed_django/index.html")
    except:
        news_feed = {"data": []}
    for post in news_feed["data"]:
        post["created_time"] = datetime.datetime.strptime(
            post["created_time"], "%Y-%m-%dT%H:%M:%S+0000") + \
            datetime.timedelta(hours=7)
    return client.render("newsfeed_django/home.html", news_feed=news_feed)


def Post(request):
    client = ClientViewHelper(request)
    message = request.POST.get("message", None)
    if not client.current_user or not message:
        return redirect("/")
    try:
        client.graph.put_wall_post(message)
    except:
        pass
    return redirect("/")

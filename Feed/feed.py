from django.contrib.syndication.views import Feed
from News.models import News


class LatestEntries(Feed):
    title = "Midnight Order"
    link = "/"
    description = "The latest news about guild."

    def item_description(self, item):
        return item.description

    def item_title(self, item):
        return item.title

    @property
    def items(self):
        return list(reversed(News.objects.all()))

    def item_link(self, item):
        return '/'
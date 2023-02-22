from django_filters import FilterSet, filters
from .models import Post

class NewsFilter(FilterSet):
    time_in = filters.DateFromToRangeFilter()

    class Meta:
       model = Post
       fields = {
           'post_name': ['icontains'],
           'post_type': ['exact'],
           'post_cat' :['exact'],
       }
import datetime
from haystack import indexes
from lookingglass_app.models import Tags, Sources, Image


class ImageIndex(indexes.SearchIndex, indexes.Indexable):
    text    = indexes.CharField(document=True, use_template=True)
    url     = indexes.CharField(model_attr='url')
    tags    = indexes.MultiValueField()
    source  = indexes.MultiValueField()    

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
    def get_model(self):
        return Image

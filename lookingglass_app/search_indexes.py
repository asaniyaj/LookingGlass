from haystack import indexes
from lookingglass_app.models import Tag, Source, Image


class ImageIndex(indexes.SearchIndex, indexes.Indexable):
    text    = indexes.CharField(document=True, use_template=True)
    url     = indexes.CharField(model_attr='url')
    tag     = indexes.CharField(model_attr='tag')
    source  = indexes.CharField(model_attr='source')
    #tags = indexes.MultiValueField()
    #source  = indexes.MultiValueField()    

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
    def get_model(self):
        return Image
    
class SourceIndex(indexes.SearchIndex, indexes.Indexable):
    text    = indexes.CharField(document=True, use_template=True)
    name     = indexes.CharField(model_attr='name')    

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
    def get_model(self):
        return Source
    
class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text    = indexes.CharField(document=True, use_template=True)
    name     = indexes.CharField(model_attr='name')    

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
    def get_model(self):
        return Tag

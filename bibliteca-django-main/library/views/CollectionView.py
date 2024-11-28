from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Collection


# Collection Views
class CollectionListView(ListView):
    model = Collection
    template_name = 'collection_list.html'
    context_object_name = 'collections'


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collection_detail.html'
    context_object_name = 'collection'

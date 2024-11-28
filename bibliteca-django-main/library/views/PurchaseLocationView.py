from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import PurchaseLocation

# Purchase Location Views
class PurchaseLocationListView(ListView):
    model = PurchaseLocation
    template_name = 'purchase_location_list.html'
    context_object_name = 'locations'


class PurchaseLocationDetailView(DetailView):
    model = PurchaseLocation
    template_name = 'purchase_location_detail.html'
    context_object_name = 'location'

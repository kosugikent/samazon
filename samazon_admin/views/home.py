from django.shortcuts import redirect
from django.views.generic import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect('samazon_admin:category_list')

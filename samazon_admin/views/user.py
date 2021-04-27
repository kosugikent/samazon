from datetime import datetime

from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import View

from core.models import User
from core.views.mixins import PaginationMixin


class UserListView(PaginationMixin, View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        if 'keyword' in request.GET:
            q = Q()
            for field_name in ('username', 'email', 'phone', 'postal_code', 'address'):
                q |= Q(**{f'{field_name}__contains': request.GET['keyword']})
            users = users.filter(q)
        context = self.get_page_data(users)
        return render(request, 'samazon_admin/user/list.html', context)


class UserDeleteReviveView(View):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        User.objects.filter(pk=kwargs['pk']).update(deleted_at=datetime.now() if not user.deleted_at else None)
        return redirect('samazon_admin:user_list')

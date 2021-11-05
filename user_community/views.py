from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, FormView
from user_community.forms import CommunityCreateForm, CommunityEditForm
from user_community.models import Community, CommunitySubscriber, CommunitySubscribeRequest
from user_community.utils import get_community_state
from user_note.forms import PostAddForm


User = get_user_model()


'''Separate community page view'''
class CommunityPageView(LoginRequiredMixin, DetailView, FormView):
    model = Community
    template_name = 'community_page.html'
    context_object_name = 'community'
    slug_url_kwarg = 'community_id'
    form_class = PostAddForm

    def get_success_url(self):
        return reverse_lazy(
            'community_page',
            kwargs={
                'community_id': self.kwargs.get('community_id')
            }
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )

    def get_context_data(self, **kwargs):
        community = get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )
        context = super().get_context_data(**kwargs)
        context['title'] = community.name
        context['authorized_user'] = self.request.user
        context['community_state'] = get_community_state(
            context['authorized_user'],
            community,
        )
        return context
    
    def form_valid(self, form):
        form.save(community=self.get_object())
        return super(CommunityPageView, self).form_valid(form)


'''View on which the filtered list of communities is shown'''
class CommunityListView(LoginRequiredMixin, ListView):
    model = Community
    template_name = 'community_list.html'
    context_object_name = 'communities'

    def get_queryset(self):
        return self.request.user.community_subscribes.all()


'''View of community creation page'''
class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    template_name = 'community_create.html'
    form_class = CommunityCreateForm

    def form_valid(self, form):
        print(form.cleaned_data)
        form.fields['staff_list'] = self.request.user
        form.save()
        return redirect(
            'community_page',
            community_id=Community.objects.get(name=form.cleaned_data.get('name')).community_id
        )

    def get_success_url(self):
        return reverse_lazy(
        'community_page',
        kwargs={
            'community_id': self.kwargs['community_id'],
        }
    )


'''
View to edit the community settings, 
only community staff can do so
'''
class CommunityEditView(LoginRequiredMixin, UpdateView):
    model = Community
    template_name = 'community_edit.html'
    context_object_name = 'community'
    slug_url_kwarg = 'community_id'
    form_class = CommunityEditForm

    def get_object(self, queryset=None):
        return get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )

    def get_success_url(self):
        return reverse_lazy(
        'community_page',
        kwargs={
            'community_id': self.kwargs['community_id'],
        }
    )


'''
View to delete the community,
only community staff can do so
'''
class CommunityDeleteView(LoginRequiredMixin, DeleteView):
    model = Community
    template_name = 'community_delete.html'
    context_object_name = 'community'
    slug_url_kwarg = 'community_id'
    success_url = reverse_lazy('community_list')

    def get_object(self, queryset=None):
        return get_object_or_404(
            Community,
            community_id=self.kwargs.get('community_id')
        )


'''View of sending subscribe request to private community'''
@login_required
def subscribe_view(request, community_id):
    if request.user.is_active:
        community = get_object_or_404(Community, community_id=community_id)
        if community.is_public:
            subscriber = CommunitySubscriber(
                from_user=request.user,
                to_community=community,
            )
            subscriber.save()
            request.user.community_subscribes.add(community)
        else:
            subscribe_request = CommunitySubscribeRequest(
                from_user=request.user,
                to_community=community,
                state=None,
            )
            subscribe_request.save()
            community.subscribe_requests.add(subscribe_request)
        return redirect('community_page', community_id)
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect('error.html', context=context)


@login_required
def unsubscribe_view(request, community_id):
    if request.user.is_active:
       try:
           request.user.community_subscribes.get(community_id=community_id).delete()
           CommunitySubscriber.objects.get(from_user=request.user).delete()
       except:
           pass
       return redirect('community_page', community_id)
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect('error.html', context=context)

'''View of answering on subscribe request'''
@login_required
def subscribe_request_result(request, user_id, community_id, result):
    if request.user.is_active:
        request_user = get_object_or_404(User, user_id=user_id)
        community = get_object_or_404(Community, community_id=community_id)
        if result == 'accept':
            subscriber = CommunitySubscriber(
                from_user=request_user,
                to_community=community,
            )
            subscriber.save()
            request_user.community_subscribes.add(community)
        community.subscribe_requests.get(from_user=request_user).delete()
        return redirect('subscribe_requests')
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect('error.html', context=context)

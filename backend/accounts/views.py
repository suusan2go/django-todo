from django.contrib.auth import login
from django.core.signing import loads, SignatureExpired, BadSignature

from accounts.models import User
from libs.ajax_login_required import ajax_login_required
from todoapp import settings
from .forms import UserCreationForm
from django.http import Http404, JsonResponse, HttpResponseBadRequest


timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内


@ajax_login_required
def show(request):
    user = request.user
    return JsonResponse({
        'user': {
            'id': user.id,
            'email': user.email
        }
    })


def create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return JsonResponse({
                "user": {
                    'id': user.id,
                    'email': user.email
                }
            })
    else:
        raise Http404


def confirm(request, **kwargs):
    if request.method == 'POST':
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoenNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return JsonResponse({'user': {'id': user.id, 'email': user.email}})
        return HttpResponseBadRequest()

    else:
        raise Http404


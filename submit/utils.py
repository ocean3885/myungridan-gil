from django.shortcuts import redirect
from datetime import datetime
from functools import wraps
from django.core.cache import cache

def staff_check(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

def staff_or_valid_session_check(user, request):
    # 사용자가 스태프이거나 관리자인지 확인
    staff_or_admin = user.is_authenticated and (user.is_superuser or user.is_staff)
    
    # 세션에서 이름과 전화번호를 확인
    valid_session = 'submit_name' in request.session 

    return staff_or_admin or valid_session

def user_passes_test_with_request(test_func):
    """request 객체를 테스트 함수에 전달하기 위한 데코레이터를 생성하는 팩토리 함수"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, request):
                return view_func(request, *args, **kwargs)
            return redirect('/')
        return _wrapped_view
    return decorator

def get_client_ip(request):
    """요청에서 클라이언트 IP 주소를 가져오는 함수"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_rate_limited(cache_key, limit_seconds):
    """속도 제한 여부를 확인하는 함수"""
    last_post_time = cache.get(cache_key)
    if last_post_time:
        elapsed_time = (datetime.now() - last_post_time).total_seconds()
        if elapsed_time < limit_seconds:
            return True, limit_seconds - elapsed_time  # 제한 상태와 남은 시간 반환
    return False, None

def update_last_post_time(cache_key, timeout=30):
    """현재 시간을 캐시에 갱신"""
    cache.set(cache_key, datetime.now(), timeout=timeout)
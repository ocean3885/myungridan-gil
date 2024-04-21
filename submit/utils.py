from django.shortcuts import redirect

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
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, request):
                return view_func(request, *args, **kwargs)
            return redirect('/')
        return _wrapped_view
    return decorator
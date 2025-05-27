from django import template
import re

register = template.Library()

@register.filter(name='hanja_color')
def get_class_by_element(element):
# 각 요소에 대한 배경색과 텍스트색 매핑
    class_map = {
    '甲': 'bg-lime-100 text-black',
    '乙': 'bg-lime-200 text-black',
    '丙': 'bg-red-200 text-black',
    '丁': 'bg-red-100 text-black',
    '戊': 'bg-orange-200 text-black',
    '己': 'bg-orange-300 text-black',
    '庚': 'bg-slate-100 text-black',
    '辛': 'bg-slate-200 text-black',
    '壬': 'bg-blue-100 text-black',
    '癸': 'bg-blue-200 text-black',
    '子': 'bg-blue-200 text-black',
    '丑': 'bg-orange-300 text-black',
    '寅': 'bg-lime-100 text-black',
    '卯': 'bg-lime-200 text-black',
    '辰': 'bg-orange-200 text-black',
    '巳': 'bg-red-200 text-black',
    '午': 'bg-red-100 text-black',
    '未': 'bg-orange-300 text-black',
    '申': 'bg-slate-100 text-black',
    '酉': 'bg-slate-200 text-black',
    '戌': 'bg-orange-200 text-black',
    '亥': 'bg-blue-100 text-black',
    }
    return class_map.get(element, 'bg-gray-300 text-black') # 기본값 설정

@register.filter
def mask_name(name):
    if not name:
        return ''
    return ''.join(char if i % 2 == 0 else 'ㅇ' for i, char in enumerate(name))

@register.filter(name='zeropad')
def zeropad(value):
    """
    한 자리 숫자를 2자리로 만들어주는 필터. (예: 1 -> "01", 10 -> "10")
    숫자가 아닌 값이 들어올 경우를 대비하여 예외 처리를 포함합니다.
    """
    try:
        # 값을 문자열로 변환한 뒤, zfill(2)를 사용하여 전체 길이를 2로 만들고
        # 부족한 앞자리를 '0'으로 채웁니다.
        return str(value).zfill(2)
    except (ValueError, TypeError):
        # 만약 값이 숫자나 문자열로 변환될 수 없는 경우, 원래 값을 그대로 반환
        return value
    
@register.filter(name='two_digits')
def last_two_digits(value):
    """
    값(숫자 또는 문자)을 문자열로 변환하여 마지막 두 자리만 반환하는 필터.
    (예: 2024 -> "24", 1998 -> "98")
    """
    try:
        # 값을 문자열로 변환
        s = str(value)
        # 문자열 슬라이싱을 사용하여 뒤에서부터 2개의 문자를 가져옴
        return s[-2:]
    except (ValueError, TypeError):
        # 변환에 실패하면 원래 값을 그대로 반환
        return value
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


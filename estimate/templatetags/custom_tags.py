from django import template

register = template.Library()

@register.filter(name='custom_filter')
def get_class_by_element(element):
# 각 요소에 대한 배경색과 텍스트색 매핑
    class_map = {
    '甲': 'bg-red-500 text-white',
    '乙': 'bg-blue-500 text-white',
    '丙': 'bg-green-500 text-white',
    '丁': 'bg-yellow-500 text-black',
    '戊': 'bg-orange-500 text-white',
    '己': 'bg-teal-500 text-white',
    '庚': 'bg-purple-500 text-white',
    '辛': 'bg-pink-500 text-white',
    '壬': 'bg-lime-500 text-black',
    '癸': 'bg-cyan-500 text-white',
    '子': 'bg-red-600 text-white',
    '丑': 'bg-blue-600 text-white',
    '寅': 'bg-green-600 text-white',
    '卯': 'bg-yellow-600 text-black',
    '辰': 'bg-orange-600 text-white',
    '巳': 'bg-teal-600 text-white',
    '午': 'bg-purple-600 text-white',
    '未': 'bg-pink-600 text-white',
    '申': 'bg-lime-600 text-black',
    '酉': 'bg-cyan-600 text-white',
    '戌': 'bg-red-700 text-white',
    '亥': 'bg-blue-700 text-white',
    }
    return class_map.get(element, 'bg-gray-300 text-black') # 기본값 설정
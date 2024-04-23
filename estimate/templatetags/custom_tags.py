from django import template

register = template.Library()


# 한글에서 한자로의 매핑
korean_to_hanja = {
    '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
    '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸',
    '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰',
    '사': '巳', '오': '午', '미': '未', '신': '申', '유': '酉',
    '술': '戌', '해': '亥'
}

@register.filter(name='to_hanja')
def to_hanja(korean_text):
    return ''.join(korean_to_hanja.get(char, char) for char in korean_text)


@register.filter(name='reverse')
def reverse_list(value):
    try:
        return list(reversed(value))
    except TypeError:
        return value  # 입력 값이 리스트가 아닐 경우 원래 값을 그대로 반환

@register.filter(name='hanja_color')
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

@register.filter(name='kor_color')
def get_class_by_element(element):
# 각 요소에 대한 배경색과 텍스트색 매핑
    class_map = {
    '갑': 'bg-red-500 text-white',
    '을': 'bg-blue-500 text-white',
    '병': 'bg-green-500 text-white',
    '정': 'bg-yellow-500 text-black',
    '무': 'bg-orange-500 text-white',
    '기': 'bg-teal-500 text-white',
    '경': 'bg-purple-500 text-white',
    '신': 'bg-pink-500 text-white',
    '임': 'bg-lime-500 text-black',
    '계': 'bg-cyan-500 text-white',
    '자': 'bg-red-600 text-white',
    '축': 'bg-blue-600 text-white',
    '인': 'bg-green-600 text-white',
    '묘': 'bg-yellow-600 text-black',
    '진': 'bg-orange-600 text-white',
    '사': 'bg-teal-600 text-white',
    '오': 'bg-purple-600 text-white',
    '미': 'bg-pink-600 text-white',
    '신': 'bg-lime-600 text-black',
    '유': 'bg-cyan-600 text-white',
    '술': 'bg-red-700 text-white',
    '해': 'bg-blue-700 text-white',
    }
    return class_map.get(element, 'bg-gray-300 text-black') # 기본값 설정
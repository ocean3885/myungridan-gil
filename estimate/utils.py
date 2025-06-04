import requests
import json
from .models import InmyungHanja
from pathlib import Path

ELEMENT_MAP = {
    "甲": "목",
    "乙": "목",
    "丙": "화",
    "丁": "화",
    "戊": "토",
    "己": "토",
    "庚": "금",
    "辛": "금",
    "壬": "수",
    "癸": "수",
    # 지지도
    "子": "수",
    "丑": "토",
    "寅": "목",
    "卯": "목",
    "辰": "토",
    "巳": "화",
    "午": "화",
    "未": "토",
    "申": "금",
    "酉": "금",
    "戌": "토",
    "亥": "수",
}

def count_elements(chars: str) -> dict:
    """
    한문 8글자 입력 받아서 목화토금수 개수를 dict로 반환
    chars: 문자열, 최대 8글자
    """
    counts = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
    chars = chars[:8]  # 최대 8글자만 처리

    for ch in chars:
        element = ELEMENT_MAP.get(ch)
        if element:
            counts[element] += 1

    return counts

def fetch_estimate_data_from_api(year, month, day, hour, minute, sl, gen):
    """
    외부 express API에 요청 보내고 결과 JSON 반환
    필요한 파라미터 맞춰서 넘겨주세요.
    """
    EXPRESS_API_ENDPOINT = "https://namaste23.cafe24.com/api"
    
    params = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "min": minute,
        "gender": gen,
        "calendar_type": sl,
    }
    
    try:
        response = requests.get(EXPRESS_API_ENDPOINT, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # 에러 처리 로깅 등 필요하면 여기에 추가
        return None
    
def get_hanja_details_as_json(hanja_text):
    """
    한자 텍스트(2~4글자)를 입력받아 각 글자의 상세 정보를 JSON 형태로 반환합니다.

    Args:
        hanja_text (str): 2~4글자의 한자 문자열

    Returns:
        str: 각 한자 글자의 정보가 담긴 JSON 문자열.
             오류 발생 시 또는 글자를 찾지 못했을 경우 빈 리스트 또는 해당 글자 정보 누락.
    """
    if not (2 <= len(hanja_text) <= 4):
        # 또는 적절한 예외 처리를 할 수 있습니다.
        return json.dumps({"error": "한자 텍스트는 2~4글자여야 합니다."}, ensure_ascii=False)

    results = []
    for char_input in hanja_text:
        try:
            hanja_obj = InmyungHanja.objects.get(char=char_input)
            char_data = {
                'char': hanja_obj.char,
                'pron': hanja_obj.pron,
                'main_mean': hanja_obj.main_mean,
                'main_elem': hanja_obj.main_elem,
                'disused': hanja_obj.disused,
                'tot_stk': hanja_obj.tot_stk,
                'rad_stk': hanja_obj.rad_stk,
                'rad_elem': hanja_obj.rad_elem,
                'detail_mean': hanja_obj.detail_mean,
            }
            results.append(char_data)
        except InmyungHanja.DoesNotExist:
            # 해당 한자를 찾지 못한 경우, 결과에 포함하지 않거나 오류 메시지를 추가할 수 있습니다.
            # 여기서는 찾지 못한 글자는 결과에서 제외합니다.
            # 필요하다면 아래와 같이 처리할 수 있습니다:
            # results.append({'char': char_input, 'error': '정보를 찾을 수 없습니다.'})
            print(f"Warning: '{char_input}'에 대한 정보를 InmyungHanja 모델에서 찾을 수 없습니다.")
            pass
        except Exception as e:
            # 기타 예외 처리
            print(f"Error processing '{char_input}': {e}")
            # results.append({'char': char_input, 'error': str(e)})
            pass

    return results


def get_name_suri_details(json_output):
    """
    한자 이름 정보와 수리 데이터를 받아, 획수에 맞는 상세 정보를 반환합니다.

    Args:
        json_output (list): 각 한자 정보를 담은 딕셔너리의 리스트.
        suri_filepath (str): 81수리 데이터가 있는 JSON 파일 경로.

    Returns:
        dict: 'won', 'hyung', 'lee', 'jeong'에 해당하는 81수리 상세 정보를 담은 딕셔너리.
              에러 발생 시 에러 메시지를 담은 딕셔너리를 반환합니다.
    """
    current_file_path = Path(__file__)
    suri_filepath = current_file_path.parent / 'data' / '81suri.json'
    # 1. 81수리 데이터 로드 및 number를 키로 하는 딕셔너리로 변환
    try:
        with open(suri_filepath, 'r', encoding='utf-8') as f:
            suri_data = json.load(f)
        suri_map = {item['number']: item for item in suri_data}
    except FileNotFoundError:
        # 경로를 동적으로 계산했으므로, 이 에러는 파일이 실제로 없을 때만 발생합니다.
        return {"error": f"파일을 찾을 수 없습니다: {suri_filepath}"}
    except json.JSONDecodeError:
        return {"error": f"JSON 파일 형식이 올바르지 않습니다: {suri_filepath}"}

    # 2. 이름 글자 수에 따라 획수 계산
    num_chars = len(json_output)
    strokes = [item.get('tot_stk', 0) for item in json_output]
    total_strokes = sum(strokes)
    
    calculated_nums = {}

    if num_chars == 2:
        calculated_nums['won'] = strokes[1]
        calculated_nums['hyung'] = total_strokes
        calculated_nums['jeong'] = total_strokes
        calculated_nums['lee'] = strokes[0]
    elif num_chars == 3:
        calculated_nums['won'] = strokes[1] + strokes[2]
        calculated_nums['hyung'] = strokes[0] + strokes[1]
        calculated_nums['lee'] = strokes[0] + strokes[2]
        calculated_nums['jeong'] = total_strokes
    elif num_chars == 4:
        calculated_nums['won'] = strokes[2] + strokes[3]
        calculated_nums['hyung'] = strokes[1] + strokes[2]
        calculated_nums['lee'] = strokes[0] + strokes[3]
        calculated_nums['jeong'] = total_strokes
    else:
        return {"error": f"이름 글자 수는 2, 3, 4글자만 지원합니다. 입력된 글자 수: {num_chars}"}

    # 3. 계산된 획수(숫자)를 81수리 데이터 객체로 매핑
    result = {}
    for key, number in calculated_nums.items():
        # .get()을 사용하여 해당 number가 suri_map에 없으면 None을 반환
        result[key] = suri_map.get(number)

    return result


def get_name_five_elements_string(name):
    """
    이름을 입력받아 각 글자의 초성 오행을 분석하여 문자열 형태로 반환하는 함수.

    Args:
        name (str): 분석할 한글 이름.

    Returns:
        str: 각 글자의 초성 오행을 연결한 문자열.
             예: '土木火', '土木', '土木土木'
             한글이 아닌 문자는 무시됩니다.
    """

    # 한글 유니코드 범위
    # 초성, 중성, 종성을 분리하기 위한 유니코드 기준점
    CHOSUNG_START_CODE = 0x1100

    # 한글 초성 리스트
    chosung_list = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
        'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]

    # 초성 오행 매핑 (일반적인 성명학 기준)
    chosung_five_elements_map = {
        'ㄱ': '木', 'ㅋ': '木',
        'ㄴ': '火', 'ㄷ': '火', 'ㄹ': '火', 'ㅌ': '火',
        'ㅇ': '土', 'ㅎ': '土',
        'ㅅ': '金', 'ㅈ': '金', 'ㅊ': '金',
        'ㅁ': '水', 'ㅂ': '水', 'ㅍ': '水'
    }

    five_elements_sequence = [] # 오행 결과를 저장할 리스트

    for char in name:
        # 한글이 아닐 경우 스킵
        if not ('\uAC00' <= char <= '\uD7A3'):
            continue

        # 한글 한 글자를 초성, 중성, 종성으로 분리
        char_code = ord(char) - 0xAC00

        # 초성 인덱스 계산
        chosung_idx = char_code // (21 * 28)
        
        # 초성 문자 추출
        chosung = chosung_list[chosung_idx]

        # 초성 오행 분류
        five_element = "" # 기본값은 빈 문자열
        if chosung in chosung_five_elements_map:
            five_element = chosung_five_elements_map[chosung]
        # 된소리 처리 (ㄲ, ㄸ, ㅃ, ㅆ, ㅉ)
        elif chosung == 'ㄲ': five_element = chosung_five_elements_map['ㄱ']
        elif chosung == 'ㄸ': five_element = chosung_five_elements_map['ㄷ']
        elif chosung == 'ㅃ': five_element = chosung_five_elements_map['ㅂ']
        elif chosung == 'ㅆ': five_element = chosung_five_elements_map['ㅅ']
        elif chosung == 'ㅉ': five_element = chosung_five_elements_map['ㅈ']
        
        # 오행이 분류되었으면 리스트에 추가
        if five_element:
            five_elements_sequence.append(five_element)

    return "".join(five_elements_sequence)


def get_suri_ohaeng_combination(stroke_counts: list[int]) -> str:
    """
    이름 각 글자의 획수 리스트를 입력받아 각 획수의 수리오행을 조합하여 반환합니다.

    Args:
        stroke_counts (list[int]): 이름 각 글자의 획수 리스트 (2~4개)

    Returns:
        str: 각 획수의 수리오행을 조합한 문자열 (예: 목목수, 수목화)
             유효하지 않은 입력(획수 개수, 음수 획수)의 경우 오류 메시지 반환
    """
    if not (2 <= len(stroke_counts) <= 4):
        return "오류: 획수 정보는 2개에서 4개까지 입력할 수 있습니다."

    # 획수 끝자리와 오행 매핑
    ohaeng_mapping_by_digit = {
        1: "木", 2: "木",
        3: "火", 4: "火",
        5: "土", 6: "土",
        7: "金", 8: "金",
        9: "水", 0: "水"
    }

    result_ohaengs = []
    for count in stroke_counts:
        if count < 0:
            return "오류: 획수는 음수가 될 수 없습니다."

        last_digit = count % 10
        # last_digit은 0-9 사이이므로 반드시 ohaeng_mapping_by_digit에 존재합니다.
        result_ohaengs.append(ohaeng_mapping_by_digit[last_digit])

    return "".join(result_ohaengs)


def analyze_ohaeng_harmony(ohaeng_combination: str) -> str:
    """
    오행 조합 문자열을 입력받아 상생 및 상극 관계를 분석하여 이름의 조화를 평가합니다.

    Args:
        ohaeng_combination (str): 각 글자의 수리오행이 조합된 문자열 (예: "목목수", "수목화")

    Returns:
        str: 이름의 조화 평가 ("좋음", "보통", "나쁨")
             유효하지 않은 입력의 경우 오류 메시지 반환
    """
    if not isinstance(ohaeng_combination, str) or len(ohaeng_combination) < 2:
        return "오류: 오행 조합 문자열은 최소 2글자 이상이어야 합니다."

    # 상생 관계 정의 (현재 오행이 다음 오행을 생성)
    sang_saeng_rules = {
        '木': '火',
        '火': '土',
        '土': '金',
        '金': '水',
        '水': '木'
    }

    # 상극 관계 정의 (현재 오행이 다음 오행을 극복하거나, 다음 오행이 현재 오행을 극복)
    sang_geuk_rules = {
        '木': '土', # 목 극 토
        '火': '金', # 화 극 금
        '土': '水', # 토 극 수
        '金': '木', # 금 극 목
        '水': '火'  # 수 극 화
    }

    # 유효한 오행 글자 목록 (입력 유효성 검사용)
    valid_ohaengs = {'木', '火', '土', '金', '水'}

    sang_saeng_count = 0
    sang_geuk_count = 0
    total_pairs = len(ohaeng_combination) - 1

    for i in range(total_pairs):
        current_ohaeng = ohaeng_combination[i]
        next_ohaeng = ohaeng_combination[i+1]

        # 입력된 오행 글자의 유효성 검사
        if current_ohaeng not in valid_ohaengs or next_ohaeng not in valid_ohaengs:
            return "오류: 유효하지 않은 오행 글자가 포함되어 있습니다."

        # 상생 관계 확인 (current -> next)
        if sang_saeng_rules.get(current_ohaeng) == next_ohaeng:
            sang_saeng_count += 1
        elif sang_saeng_rules.get(next_ohaeng) == current_ohaeng:
            sang_saeng_count += 1
        # 상극 관계 확인 (current -> next)
        elif sang_geuk_rules.get(current_ohaeng) == next_ohaeng:
            sang_geuk_count += 1
        # 역방향 상극 관계 확인 (next -> current)
        elif sang_geuk_rules.get(next_ohaeng) == current_ohaeng:
            sang_geuk_count += 1

    # 평가 로직
    # 1. 상생으로만 구성되면 '좋음'
    if sang_geuk_count == 0 and sang_saeng_count > 0:
        return "좋음"
    # 2. 상생 비율이 높으면 '보통' (상극 관계가 없거나 상생 관계가 더 많을 때)
    elif sang_saeng_count > sang_geuk_count:
        return "보통"
    # 3. 상극 비율이 높으면 '나쁨' (상극 관계가 상생 관계보다 많거나 같을 때,
    #    또는 상생/상극 관계가 모두 없을 때도 나쁨으로 간주)
    else:
        return "나쁨"
    
    
def extract_tot_stk_values(data_list: list[dict]) -> list[int]:
    """
    딕셔너리를 요소로 갖는 리스트를 입력받아 각 딕셔너리의 'tot_stk' 값을 추출하여
    새로운 정수형 리스트로 반환합니다.

    Args:
        data_list (list[dict]): 딕셔너리 요소 2개에서 4개로 구성된 리스트.
                                각 딕셔너리는 'tot_stk' 키를 포함해야 합니다.

    Returns:
        list[int]: 추출된 'tot_stk' 값들의 리스트.
                   입력 유효성 검사 실패 시 빈 리스트 또는 오류를 나타내는 값을 반환할 수 있으나,
                   예시에서는 기본적인 추출 로직을 따릅니다.
    """
    # 1. 입력 리스트의 요소 개수 확인
    if not (2 <= len(data_list) <= 4):
        print("오류: 입력 리스트는 2개에서 4개의 딕셔너리 요소를 포함해야 합니다.")
        return [] # 또는 적절한 오류 처리 (예: raise ValueError)

    extracted_values = []
    for item in data_list:
        # 2. 각 요소가 딕셔너리인지 확인
        if not isinstance(item, dict):
            print(f"오류: 리스트의 요소는 딕셔너리여야 합니다. 발견된 타입: {type(item)}")
            return []

        # 3. 딕셔너리에 'tot_stk' 키가 있는지 확인
        if "tot_stk" in item:
            # 4. 'tot_stk' 값 추출 및 리스트에 추가
            extracted_values.append(item["tot_stk"])
        else:
            print(f"오류: 딕셔너리에 'tot_stk' 키가 없습니다: {item}")
            return [] # 또는 적절한 오류 처리

    return extracted_values


def extract_main_elems(dict_list):
    """
    딕셔너리를 요소로 갖는 리스트에서 각 딕셔너리의 'main_elem' 값을 추출하여 하나의 문자열로 반환합니다.
    
    :param dict_list: 2개에서 4개의 딕셔너리를 포함하는 리스트
    :return: 'main_elem' 값들을 연결한 문자열
    """
    if not (2 <= len(dict_list) <= 4):
        raise ValueError("리스트의 요소 개수는 2개에서 4개 사이여야 합니다.")
    
    return ''.join(d['main_elem'] for d in dict_list if 'main_elem' in d)

def extract_outcomes(data):
    """
    딕셔너리에서 'won', 'hyung', 'lee', 'jeong' 키에 해당하는 값들의 'outcome'을 리스트로 반환합니다.
    
    :param data: 각 키에 'outcome' 키를 포함하는 딕셔너리
    :return: outcome 값들의 리스트
    """
    keys = ["won", "hyung", "lee", "jeong"]
    return [data[key]["outcome"] for key in keys]


def evaluate_name(suri_isgood, sound_elem_isgood, suri_ohaeng_elem_isgood, jawon_isgood):
    """
    입력된 길흉 요소들을 바탕으로 전체적인 운세를 평가하여 설명 문장으로 출력합니다.
    
    :param suri_isgood: '81수리' 결과 리스트 (4개 문자열)
    :param sound_elem_isgood: 음령오행 결과 문자열
    :param suri_ohaeng_elem_isgood: 수리오행 결과 문자열
    :param jawon_isgood: 자원오행 결과 문자열
    :return: 운세 평가 설명 문장
    """
    good_keywords = ["좋음", "길"]
    bad_keywords = ["나쁨", "흉"]

    good = 0
    bad = 0

    # 수리 결과 4개 평가
    for result in suri_isgood:
        if any(word in result for word in good_keywords):
            good += 1
        if any(word in result for word in bad_keywords):
            bad += 1

    # 나머지 요소 평가
    for elem in [sound_elem_isgood, suri_ohaeng_elem_isgood, jawon_isgood]:
        if any(word in elem for word in good_keywords):
            good += 2
        if any(word in elem for word in bad_keywords):
            bad += 2

    # 총평 판단
    if bad == 0 and good > 0:
        result_comment = (
        "이 이름은 전반적으로 매우 길한 요소들로 구성되어 있어 매우 좋은 인상을 줍니다. "
        "모든 평가 항목에서 긍정적인 결과가 도출되어, 안정감과 조화를 갖춘 이상적인 이름이라 할 수 있습니다."
        )
    elif good > bad:
        result_comment = (
        "이 이름은 대체로 긍정적인 방향으로 해석됩니다. 여러 요소에서 길한 의미가 포함되어 있으며, "
        "전반적인 조화와 흐름이 나쁘지 않아 무난하고 좋은 이름으로 평가될 수 있습니다. "
        "다만 일부 요소는 보완의 여지가 있어 참고할 필요가 있습니다."
        )
    elif bad > good:
        result_comment = (
        "이 이름은 다소 아쉬운 면이 존재합니다. 여러 평가 항목에서 흉한 의미가 나타나고 있어, "
        "이름을 사용할 때 주의가 요구됩니다. 의미적인 측면이나 조화의 부족이 문제로 작용할 수 있으므로, "
        "추가적인 보완이나 대안 검토가 필요할 수 있습니다."
        )
    else:
        result_comment = (
        "이 이름은 길한 요소와 흉한 요소가 혼재되어 있어 해석이 분분할 수 있습니다. "
        "어떤 측면에서는 긍정적인 의미를 가지지만, 다른 측면에서는 다소 부정적인 신호도 포함하고 있어 "
        "이름을 결정하기 전 충분한 숙고와 전문가의 조언을 받는 것이 바람직합니다."
        )

    return result_comment

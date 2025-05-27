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
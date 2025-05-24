import requests

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
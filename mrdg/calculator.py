def find_ten_god(benchmark, other):
    # 천간 배열
    heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    
    # 천간 인덱스 찾기
    index_b = heavenly_stems.index(benchmark)
    index_o = heavenly_stems.index(other)
    
    # 십성 관계 정의
    relationships = {
        0: '비견',   # 같은 것
        1: '겁재',   # 같은 것의 다른 측면 (긍정적/부정적)
        2: '식신',   # 생성하는 것
        3: '상관',   # 생성하려는 것을 제어
        4: '편재',   # 제어하려는 것의 다른 형태
        5: '정재',   # 제어하려는 것을 강화
        6: '편관',   # 강화하려는 것을 제압
        7: '정관',   # 제압하려는 것을 지원
        8: '편인',   # 지원하려는 것의 다른 형태
        9: '정인',   # 지원하려는 것을 생성
        -1: '정재',  # 생성하려는 것의 다른 형태
        -2: '편재',  # 강화하려는 것의 다른 형태
        -3: '정관',  # 제압하려는 것의 다른 형태
    }
    
    # 인덱스 차이 계산
    difference = (index_o - index_b) % 10
    
    # 십성 반환
    return relationships.get(difference, "관계 없음")


def find_stem_branch_ten_god(stem, branch):
    # 천간 배열
    heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    # 지지 배열
    earthly_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    # 지지와 천간의 상호작용을 기반으로 십성을 정의하는 규칙 (예제)
    interaction = {
        '갑': {'자': '비견', '축': '겁재', '인': '비견', '묘': '겁재'},
        '기': {'축': '비견', '미': '비견'}
    }
    
    # 천간을 기준으로 해당 지지의 십성을 찾기
    if stem in interaction and branch in interaction[stem]:
        return interaction[stem][branch]
    
    # 십성이 정의되지 않은 경우
    return "관계 없음"


def find_twelve_luck(stem, branch):
    # 지지 배열
    earthly_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    # 십이운성 배열
    twelve_lucks = ['장생', '목욕', '관대', '건록', '제왕', '쇠', '병', '사', '묘', '절', '태', '양']
    
    # 천간별 시작 지지와 순서 정의
    start_branches = {
        '갑': ('해', False), '을': ('미', True), '병': ('인', False),
        '정': ('술', True), '무': ('인', False), '기': ('술', True),
        '경': ('사', False), '신': ('축', True), '임': ('신', False),
        '계': ('진', True)
    }
    
    start_branch, reverse = start_branches[stem]
    start_index = earthly_branches.index(start_branch)
    
    # 지지의 순서 결정
    if reverse:
        ordered_branches = list(reversed(earthly_branches[start_index:] + earthly_branches[:start_index]))
    else:
        ordered_branches = earthly_branches[start_index:] + earthly_branches[:start_index]

    luck_index = ordered_branches.index(branch)
    return twelve_lucks[luck_index]
    
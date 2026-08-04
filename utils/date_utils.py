from datetime import datetime
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")

# 현재 한국 시간
def get_korea_now() -> datetime:
    return datetime.now(KST)

# 현재 한국 날짜
def get_today() -> str:
    return get_korea_now().strftime("%Y-%m-%d")

# 한국 기준 오늘 요일
def get_today_day() -> str:
    day_map = {
        0: "월",
        1: "화",
        2: "수",
        3: "목",
        4: "금",
        5: "토",
        6: "일",
    }

    return day_map[get_korea_now().weekday()]

# 월, 수금, 화목, 토
def get_schedule_day_group() -> str | None:
    """
    오늘 요일을 schedule_master의 요일 그룹으로 변환한다.

    월요일: 월
    화요일·목요일: 화목
    수요일·금요일: 수금
    토요일: 토
    일요일: None
    """
    day_group_map = {
        "월": "월",
        "화": "화목",
        "수": "수금",
        "목": "화목",
        "금": "수금",
        "토": "토",
    }

    return day_group_map.get(get_today_day())

# 월수금, 화목토
def get_today_class_day_group() -> str | None:
    """
    한국 기준 오늘 요일을 학급 운영 요일 그룹으로 변환한다.

    월·수·금 → 월수금
    화·목·토 → 화목토
    일요일   → None
    """
    today_day = get_today_day()

    day_group_map = {
        "월": "월수금",
        "수": "월수금",
        "금": "월수금",
        "화": "화목토",
        "목": "화목토",
        "토": "화목토",
    }

    return day_group_map.get(today_day)
from datetime import datetime

from .checklist_repository import (
    load_checklist_master,
    load_daily_checklist,
    save_daily_checklist
)



def get_today():
    """
    오늘 날짜 반환
    """

    return datetime.today().strftime("%Y-%m-%d")



def create_today_checklist():
    """
    checklist_master를 기준으로
    오늘 체크리스트 생성
    """

    checklist = load_checklist_master()

    checklist.columns = checklist.columns.str.strip()

    checklist["날짜"] = get_today()

    checklist["완료여부"] = False


    return checklist



def update_check_status(
        check_id,
        class_code,
        status
):
    """
    체크 상태 저장
    """

    daily = load_daily_checklist()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # 타입 통일
    check_id = str(check_id)
    class_code = str(class_code)

    condition = (
        (daily["check_id"] == check_id)
        &
        (daily["학급코드"] == class_code)
    )

    # 조건에 맞는 데이터가 없으면 종료
    if not condition.any():
        return daily

    # 완료 여부 저장
    daily.loc[
        condition,
        "완료여부"
    ] = 1 if status else 0

    # 완료 시간 저장
    daily.loc[
        condition,
        "완료시간"
    ] = (
        now
        if status
        else ""
    )

    save_daily_checklist(
        daily
    )

    return daily
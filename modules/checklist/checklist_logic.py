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

    check_id : 체크 항목 번호
    class_code : 학급코드
    status : True / False
    """

    daily = load_daily_checklist()


    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    condition = (
        (daily["check_id"] == check_id)
        &
        (daily["학급코드"] == class_code)
    )


    daily.loc[
        condition,
        "완료여부"
    ] = status


    if status:

        daily.loc[
            condition,
            "완료시간"
        ] = now

    else:

        daily.loc[
            condition,
            "완료시간"
        ] = ""


    save_daily_checklist(daily)


    return daily
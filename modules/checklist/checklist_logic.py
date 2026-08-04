# 규칙을 처리가능하도록 설계 및 가공
from datetime import datetime
from .checklist_repository import (
    load_checklist_master,
    load_checklist_rule,
    load_class_master,
    load_schedule_master,
    load_schedule_master_target
)


# 오늘 날짜 반환
def get_today():
    return datetime.today().strftime("%Y-%m-%d")

# 오늘 요일 반환
def get_today_day():
    day_map = {
        0: "월",
        1: "화",
        2: "수",
        3: "목",
        4: "금",
        5: "토",
        6: "일",
    }
    return day_map[datetime.today().weekday()]
def get_today_day_group():
    #오늘 요일값
    today_day = get_today_day()

    day_group_map = {
        "월": "월",
        "수": "수금",
        "금": "수금",
        "화": "화목",
        "목": "화목",
        "토": "토",
    }
    return day_group_map.get(today_day)


# 체크리스트_마스터 데이터프레임 생성
def create_checklist_master():

    checklist = load_checklist_master()

    checklist.columns = checklist.columns.str.strip()

    checklist["날짜"] = get_today()

    checklist["완료여부"] = False

    return checklist

# 체크리스트_룰 데이터프레임 생성

def create_checklist_rule():

    checklist_rule = load_checklist_rule()

    return checklist_rule


# 클래스_마스터 데이터프레임 생성
def create_class_master():
    classmaster = load_class_master()

    return classmaster

# schedule_master 데이터 프레임 생성
def create_schedule_master():
    schedulemaster = load_schedule_master()

    return schedulemaster

# schedule_master_target 데이터 프레임 생성
def craete_schedule_master_target():
    schedulemaster_target = load_schedule_master_target()

    return schedulemaster_target

# 스케줄 생성 v1
# 1. 스케줄마스터-스케줄마스터타겟 schedule_id로 1대다 조인
def create_schedule_v1():
    schedule = load_schedule_master()
    target = load_schedule_master_target()

    merged_schedule = schedule.merge(
        target,
        on="schedule_id",
        how="left",
        validate="one_to_many"
    )

    return merged_schedule
# 스케줄 생성 v2
def create_schedule_v2():
    schedule = create_schedule_v1()

    today_day_group = get_today_day_group()

    #일요일
    if today_day_group is None:
        return schedule.iloc[0:0].copy()

    # 여름방학 & 현재 요일과 매칭 & 활성화 상태 체크
    today_schedule = schedule[
        (schedule["schedule_group"] == "여름방학")
        & (schedule["day_group"] == today_day_group)
        & (schedule["schedule_is_active"] == "Y")
    ].copy()

    # 시간별 순서 정렬
    today_schedule = today_schedule.sort_values(
        by="start_time"
    ).reset_index(drop=True)

    return today_schedule

# 스케줄 - 관련 마스터 데이터 전체 조인
def create_schedule_dataset():
    schedule = load_schedule_master()
    target = load_schedule_master_target()
    class_master = load_class_master()

    # 일정 1 : 대상 반 N 조인
    schedule_with_target = schedule.merge(
        target,
        on="schedule_id",
        how="left",
        validate="one_to_many"
    )

    # 대상 반 N : 학급 마스터 1 조인
    full_schedule = schedule_with_target.merge(
        class_master,
        on="class_code",
        how="left",
        validate="many_to_one"
    )
    return full_schedule

# 스케줄 - 오늘 일정에 맞게 필터링 로직
def create_today_schedule():
    schedule = create_schedule_dataset()
    today_day_group = get_today_day_group()

    if today_day_group is None:
        return schedule.iloc[0:0].copy()

    today_schedule = schedule[
        (schedule["schedule_group"] == "여름방학")
        &(schedule["day_group"] == today_day_group)
        &(schedule["schedule_is_active"] == "Y")
    ].copy()

    return(
        today_schedule
        .sort_values("start_time")
        .reset_index(drop=True)
    )

# 스케줄 - 실제 화면용 구조로 변경(그룹화)
def create_schedule_view_data():
    schedule = create_today_schedule()

    grouped_schedule = (
        schedule.groupby(
            [
                "schedule_id",
                "schedule_type",
                "start_time",
                "end_time"
            ],
            dropna=False,
            sort=False
        )
        .agg(
            class_codes=(
                "class_code",
                lambda values: list(values.dropna())
            )
        )
        .reset_index()
    )

    return grouped_schedule
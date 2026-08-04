# 규칙을 처리가능하도록 설계 및 가공
from utils.date_utils import (
    get_today,
    get_today_day,
    get_schedule_day_group,
    get_today_class_day_group
)
from .checklist_repository import (
    load_checklist_master,
    load_checklist_rule,
    load_class_master,
    load_schedule_master,
    load_schedule_master_target
)
import pandas as pd

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

    today_day_group = get_schedule_day_group()

    # 일요일
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
    today_day_group = get_schedule_day_group()

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

##################################################################
# 체크 리스트 - rule N : master 1 조인
def create_checklist_dataset():
    checklist_rule = load_checklist_rule()
    checklist_master = load_checklist_master()

    checklist = checklist_rule.merge(
        checklist_master,
        on="check_id",
        how="inner",
        validate="many_to_one"
    )

    return checklist

# 체크리스트 데이터 + 스케줄 병합해보기


# 활성화 필터링
def filter_checklist_rule_v1():
    checklist = create_checklist_dataset()

    active_checklist = checklist[
        checklist["is_active"] == "Y"
    ].copy()

    return active_checklist

# 체크리스트 룰 필터링 v2
# 활성 규칙 중 현행 또는 전체 규칙만 조회
def filter_checklist_rule_v2():
    checklist = filter_checklist_rule_v1()

    class_type_checklist = checklist[
        checklist["class_type"].isin(["현행", "전체"])
    ].copy()

    return class_type_checklist

# 체크리스트 룰 필터링 v3
# 활성 규칙 + 현행 + 부담임(또는 전체)
def filter_checklist_rule_v3():
    checklist = filter_checklist_rule_v2()

    teacher_role_checklist = checklist[
        checklist["teacher_role"].isin(
            ["부담임", "전체"]
        )
    ].copy()

    return teacher_role_checklist

# 체크리스트 룰 필터링 v4
# 활성 + 현행 + 부담임 + 월수금 조건
def filter_checklist_rule_v4():
    checklist = filter_checklist_rule_v3()

    day_type_checklist = checklist[
        checklist["day_type"].isin(
            ["월수금", "전체"]
        )
    ].copy()

    return day_type_checklist

############################# 체크리스트 룰 필터링 합치기 #############################
def filter_checklist_rules(
    apply_scope,
    class_type,
    teacher_role,
    day_type
):
    checklist = create_checklist_dataset()

    filtered = checklist[
        (checklist["is_active"] == "Y")
        & (checklist["schedule_type"].isin([apply_scope, "전체"]))
        & (checklist["class_type"].isin([class_type, "전체"]))
        & (checklist["teacher_role"].isin([teacher_role, "전체"]))
        & (checklist["day_type"].isin([day_type, "전체"]))
    ].copy()

    return filtered

# 체크리스트 <- 오늘 스케줄 첫 번째 행에 적용
def create_today_checklist_v1():
    schedule = create_today_schedule()

    # 오늘 스케줄이 없는 경우
    if schedule.empty:
        return create_checklist_dataset().iloc[0:0].copy()

    # 첫 번째 스케줄만 선택
    first_schedule = schedule.iloc[0]

    checklist = filter_checklist_rules(
        apply_scope=first_schedule["schedule_type"],
        class_type=first_schedule["class_type"],
        teacher_role=first_schedule["teacher_role"],
        day_type=first_schedule["day_group"]
    )

    return checklist

# 체크리스트 <-스케줄 1번째 행 적용 -- 필터링 추가
def create_today_checklist_v2():
    schedule = create_today_schedule()

    if schedule.empty:
        return create_checklist_dataset().iloc[0:0].copy()

    first_schedule = schedule.iloc[0]

    checklist = filter_checklist_rules(
        apply_scope=first_schedule["schedule_type"],
        class_type=first_schedule["class_type"],
        teacher_role=first_schedule["teacher_role"],
        day_type=first_schedule["day_group"]
    ).copy()

    checklist["schedule_id"] = first_schedule["schedule_id"]
    checklist["class_code"] = first_schedule["class_code"]
    checklist["start_time"] = first_schedule["start_time"]
    checklist["end_time"] = first_schedule["end_time"]

    return checklist

# 오늘 전체 체크리스트 생성
def create_today_checklist_v3():
    schedule = create_today_schedule()

    # 오늘 스케줄이 없는 경우
    if schedule.empty:
        return create_checklist_dataset().iloc[0:0].copy()

    checklist_list = []

    # 오늘 스케줄을 한 행씩 반복
    for _, schedule_row in schedule.iterrows():

        # 현재 스케줄 조건에 맞는 업무 조회
        checklist = filter_checklist_rules(
            apply_scope=schedule_row["schedule_type"],
            class_type=schedule_row["class_type"],
            teacher_role=schedule_row["teacher_role"],
            day_type=schedule_row["day_group"]
        ).copy()

        # 해당 스케줄에 적용되는 업무가 없으면 다음 일정으로 이동
        if checklist.empty:
            continue

        # 스케줄 정보를 체크리스트 각 행에 추가
        checklist["schedule_id"] = schedule_row["schedule_id"]
        checklist["class_code"] = schedule_row["class_code"]
        checklist["start_time"] = schedule_row["start_time"]
        checklist["end_time"] = schedule_row["end_time"]

        # 생성된 체크리스트를 리스트에 저장
        checklist_list.append(checklist)

    # 모든 스케줄에서 적용 업무가 없었던 경우
    if not checklist_list:
        return create_checklist_dataset().iloc[0:0].copy()

    # 각 수업별 체크리스트를 하나의 DataFrame으로 결합
    today_checklist = pd.concat(
        checklist_list,
        ignore_index=True
    )

    return today_checklist

## 일일 공통 체크리스트 만들기
def create_daily_common_checklist():
    today_day_type = get_today_class_day_group()

    if today_day_type is None:
        return create_checklist_dataset().iloc[0:0].copy()

    checklist = filter_checklist_rules(
        apply_scope="일일공통",
        class_type="전체",
        teacher_role="전체",
        day_type=today_day_type
    ).copy()

    if checklist.empty:
        return checklist

    checklist["schedule_id"] = None
    checklist["class_code"] = None
    checklist["start_time"] = None
    checklist["end_time"] = None

    return checklist

## 스케줄별 체크리스트 만들기
def create_schedule_based_checklist():
    schedule = create_today_schedule()
    checklist_list = []

    for _, schedule_row in schedule.iterrows():
        checklist = filter_checklist_rules(
            apply_scope=schedule_row["schedule_type"],
            class_type=schedule_row["class_type"],
            teacher_role=schedule_row["teacher_role"],
            day_type=schedule_row["day_group"]
        ).copy()

        if checklist.empty:
            continue

        checklist["schedule_id"] = schedule_row["schedule_id"]
        checklist["class_code"] = schedule_row["class_code"]
        checklist["start_time"] = schedule_row["start_time"]
        checklist["end_time"] = schedule_row["end_time"]

        checklist_list.append(checklist)

    if not checklist_list:
        return create_checklist_dataset().iloc[0:0].copy()

    return pd.concat(
        checklist_list,
        ignore_index=True
    )

## 일일공통 + 스케줄별 체크리스트 합치기(최종)

def create_today_checklist_v4():
    checklist_list = []

    common_checklist = create_daily_common_checklist()
    schedule_checklist = create_schedule_based_checklist()

    if not common_checklist.empty:
        checklist_list.append(common_checklist)

    if not schedule_checklist.empty:
        checklist_list.append(schedule_checklist)

    if not checklist_list:
        return create_checklist_dataset().iloc[0:0].copy()

    today_checklist = pd.concat(
        checklist_list,
        ignore_index=True
    )

    return today_checklist


# 최종 체크리스트 컬럼 추리기
def create_today_checklist_v5():
    checklist = create_today_checklist_v4()

    if checklist.empty:
        return checklist

    view_data = checklist[
        [
            "schedule_id",
            "class_code",
            "start_time",
            "end_time",
            "schedule_type",
            "category",
            "sub_category",
            "task_name",
            "description",
            "display_order"
        ]
    ].copy()

    view_data = view_data.sort_values(
        by=[
            "start_time",
            "display_order"
        ],
        na_position="first"
    ).reset_index(drop=True)

    return view_data
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


###################################
# 스케줄 생성하기_Proto
###################################
# 스케줄 생성 규칙
# 조인 -> 오늘 조건 필터 -> 오늘 스케줄

# def create_schedule():

#     # check_id 기준 inner join



#     master = load_checklist_master()
#     rule = load_checklist_rule()

#     schedule = master.merge(
#         rule,
#         on="check_id"
#         how="inner"
#     )
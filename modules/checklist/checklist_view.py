import streamlit as st

from .checklist_logic import (
    create_checklist_master,
    create_checklist_rule,
    create_class_master,
    create_schedule_master,
    craete_schedule_master_target,
    create_schedule_v1,
    create_schedule_v2,
    create_schedule_dataset,
    create_today_schedule,
    create_schedule_view_data
)

# checklist_master 데이터프레임 출력 함수
def show_checklistmaster_section():

    st.title("업무 정의")
    st.divider()

    # logic-create_checklist_master 함수 필요
    checklistmaster = create_checklist_master()

    st.dataframe(checklistmaster)

# checklist_rule 데이터프레임 출력 함수
def show_checklistrule_section():

    st.title("업무 규칙")
    st.divider()

    checklistrule = create_checklist_rule()
    st.dataframe(checklistrule)

# class_master 데이터프레임 출력
def show_classmaster_section():
    st.title("학급 정보")
    st.divider()

    classmaster = create_class_master()
    st.dataframe(classmaster)

# schedule_master 데이터프레임 출력
def show_schedule_master():
    st.title("스케줄 정보")
    st.divider()

    schedulemaster = create_schedule_master()
    st.dataframe(schedulemaster)

# schedule_master_target 데이터프레임 출력
def show_schedule_master_target():
    st.title("스케줄 타겟 정보")
    st.divider()

    schedulemaster_target = craete_schedule_master_target()
    st.dataframe(schedulemaster_target)

# 스케줄 v1 출력
def show_schedule_v1():
    st.title("스케줄 v1")
    st.divider()

    schedule = create_schedule_v1()
    st.dataframe(schedule)

def show_schedule_v2():
    st.title("오늘 스케줄 v2")
    st.divider()

    schedule = create_schedule_v2()

    if schedule.empty:
        st.info("오늘은 등록된 스케줄이 없습니다."); return

    st.dataframe(
        schedule,
        use_container_width=True,
        hide_index=True,
    )

def show_schedule_dataset():
    st.title("스케줄 데이터셋 2단 조인 출력 결과")
    st.divider()

    schedule = create_schedule_dataset()
    st.dataframe(schedule)

def show_today_schedule():
    st.title("스케줄 데이터셋 요일 필터링 로직 결과")
    st.divider()

    today_schedule = create_today_schedule()
    st.dataframe(today_schedule)

def show_today_schedule2():
    st.title("스케줄 데이터셋 그룹화 결과")
    st.divider()

    schedule = create_schedule_view_data()

    if schedule.empty:
        st.info("오늘 등록된 일정이 없습니다.")
        return

    for _, row in schedule.iterrows():
        class_text = ",".join(row["class_codes"])

        st.write(
            f"**{row['start_time']} ~ {row['end_time']}**"
        )

        st.write(
            f"**{row['schedule_type']} | {class_text}**"
        )

        st.divider()

# 최종 출력 페이지
def show_checklist_page():

    show_checklistmaster_section()
    show_checklistrule_section()
    show_classmaster_section()
    show_schedule_master()
    show_schedule_master_target()
    show_schedule_v1()
    show_schedule_v2()
    show_schedule_dataset()
    show_today_schedule()
    show_today_schedule2()

    


    # # 구분별 출력
    # categories = checklist["구분"].unique()


    # for category in categories:

    #     st.subheader(category)


    #     category_data = checklist[
    #         checklist["구분"] == category
    #     ]


    #     for _, row in category_data.iterrows():


    #         col1, col2 = st.columns(
    #             [0.1, 0.9]
    #         )


    #         with col1:

    #             checked = st.checkbox(
    #                 "",
    #                 key=f"{class_code}_{row['check_id']}"
    #             )


    #         with col2:

    #             st.write(
    #                 f"**{row['업무명']}**"
    #             )

    #             st.caption(
    #                 row["상세내용"]
    #             )

    #             st.caption(
    #                 f"대상 : {row['대상']}"
    #             )


    #         # 체크 상태 저장

    #         update_check_status(
    #             row["check_id"],
    #             class_code,
    #             checked
    #         )


    #         st.divider()
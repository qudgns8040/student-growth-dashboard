import streamlit as st

from .checklist_logic import (
    create_today_checklist,
    update_check_status
)



def show_checklist_page():
    """
    오늘 체크리스트 화면
    """

    st.title("오늘의 체크리스트")

    st.divider()


    checklist = create_today_checklist()


    # 학급코드 선택
    class_code = st.selectbox(
        "학급 선택",
        [
            "6MR1",
            "4MR",
            "7MS1",
            "7MS2"
        ]
    )


    st.divider()


    # 구분별 출력
    categories = checklist["구분"].unique()


    for category in categories:

        st.subheader(category)


        category_data = checklist[
            checklist["구분"] == category
        ]


        for _, row in category_data.iterrows():


            col1, col2 = st.columns(
                [0.1, 0.9]
            )


            with col1:

                checked = st.checkbox(
                    "",
                    key=f"{class_code}_{row['check_id']}"
                )


            with col2:

                st.write(
                    f"**{row['업무명']}**"
                )

                st.caption(
                    row["상세내용"]
                )

                st.caption(
                    f"대상 : {row['대상']}"
                )


            # 체크 상태 저장

            update_check_status(
                row["check_id"],
                class_code,
                checked
            )


            st.divider()
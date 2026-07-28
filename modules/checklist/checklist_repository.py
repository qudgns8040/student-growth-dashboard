import pandas as pd
import os

#체크리스트 데이터 폴더 위치
BASE_PATH = "data/checklist"



def load_checklist_master():
    """
    체크리스트 마스터(수업 정보) 불러오기
    """

    path = os.path.join(
        BASE_PATH,
        "checklist_master.csv"
    )

    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )



def load_checklist_history():
    """
    체크리스트 완료 기록 불러오기
    """

    path = os.path.join(
        BASE_PATH,
        "checklist_history.csv"
    )

    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )



def load_schedule_master():
    """
    시간표 마스터 불러오기
    """

    path = os.path.join(
        BASE_PATH,
        "schedule_master.csv"
    )

    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )



def load_class_master():
    """
    학급 마스터 불러오기
    """

    path = os.path.join(
        BASE_PATH,
        "class_master.csv"
    )

    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )



def load_daily_checklist():
    """
    오늘 생성된 체크리스트 불러오기
    """

    path = os.path.join(
        BASE_PATH,
        "daily_checklist.csv"
    )

    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )



def save_daily_checklist(df):
    """
    오늘 체크리스트 저장
    """

    path = os.path.join(
        BASE_PATH,
        "daily_checklist.csv"
    )

    df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig"
    )
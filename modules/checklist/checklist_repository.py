## 데이터 접근/조합을 담당하는 계층
import pandas as pd
import os

#체크리스트 데이터 위치
BASE_PATH = "data"

# checklist_master.csv 불러오기
def load_checklist_master():
    path = os.path.join(
        BASE_PATH,
        "checklist/master/checklist_master.csv"
    )

    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )

# checklist_rule.csv 불러오기
def load_checklist_rule():
    path = os.path.join(
        BASE_PATH,
        "checklist/rule/checklist_rule.csv"
    )
    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )

# class_master.csv 불러오기
def load_class_master():
    path = os.path.join(
        BASE_PATH,
        "class/master/class_master.csv"
    )
    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )
# schedule_master.csv 불러오기
def load_schedule_master():
    path = os.path.join(
        BASE_PATH,
        "schedule/master/schedule_master.csv"
    )
    return pd.read_csv(
        path,
        encoding="utf-8-sig"
    )

# schedule_master_target.csv 불러오기
def load_schedule_master_target():
    path = os.path.join(
        BASE_PATH,
        "schedule/master/schedule_master_target.csv"
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

    df = pd.read_csv(
        path,
        encoding="utf-8-sig"
    )

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 타입 통일
    df["날짜"] = df["날짜"].astype(str)
    df["check_id"] = df["check_id"].astype(str)
    df["학급코드"] = df["학급코드"].astype(str)
    df["완료여부"] = pd.to_numeric(
        df["완료여부"],
        errors="coerce"
    ).fillna(0).astype(int)

    df["완료시간"] = (
        df["완료시간"]
        .fillna("")
        .astype(str)
    )

    df["메모"] = (
        df["메모"]
        .fillna("")
        .astype(str)
    )

    return df



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
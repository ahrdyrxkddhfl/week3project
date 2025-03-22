#dotenv 모듈. .env파일에서 환경변수 불러오기 위한 라이브러리
from dotenv import load_dotenv
#환경 변수 읽기 위한 os모듈
import os
#python과 mysql 연결하기 위한 라이브러리
import pymysql

# .env 파일 불러온 뒤 환경 변수 등록
load_dotenv()

#db 연결 함수 정의
def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        charset='utf8mb4', #문자 깨지지 않도록 인코딩 설정
        cursorclass=pymysql.cursors.DictCursor #튜플이 아닌 딕셔너리 형태로. 가독성 up
    )

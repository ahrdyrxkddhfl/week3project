# app.py
#flask 모듈 가져오기, import 이용용
from flask import Flask, render_template, request, redirect, url_for

# .env 파일 이용. pw 하드 코딩 피하기, 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()

#mysql 계정 연결 테스트 확인용/나중에 삭제하기
import os
os.environ["DB_USER"] = "roseblue"
print("💡 DB_USER:", os.getenv("DB_USER"))
print("💡 DB_PASSWORD:", os.getenv("DB_PASSWORD"))

#db 연결 함수 import. db.py에 따로 정의되어 있어야 함 주의.
from db import get_conn

app = Flask(__name__)

#메인 페이지
@app.route("/")
def index():
    conn = get_conn() #db연결
    cur = conn.cursor() #cursor 생성 : 말할 사람, 주체
    cur.execute("SELECT * FROM posts ORDER BY id DESC") #sql 실행. 명령 내용. 즉 질문 행위.
    posts = cur.fetchall() #질문하고 돌아온 응답 듣기 : 작성된 글 전부 보이게 하기
    conn.close()
    return render_template("index.html", posts=posts) #index.html이 posts 변수 사용할 수 있도록. flask가 index.html 렌더링할때 posts 데이터 넘겨줌

#게시판에 글 작성. GET을 통해 입력, POST로 입력된 내용 제출
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"] #GET으로 입력한 폼 중 제목 부분 가져오고
        content = request.form["content"] #내용 가져오기
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        conn.commit() #db 수정
        conn.close()
        return redirect(url_for("index")) #메인 페이지로 이동
    return render_template("create.html") #GET요청이면 create.html 폼

#작성한 게시글 수정하기. GET으로 기존 내용 보여주고, POST로 수정 내용 반영
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_conn()
    cur = conn.cursor()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        cur.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s", (title, content, id)) #수정할 게시글
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    cur.execute("SELECT * FROM posts WHERE id=%s", (id,))
    post = cur.fetchone()
    conn.close()
    return render_template("edit.html", post=post) #수정하려고 페이지 진입하면, 수정 전 원래ver 글 보여줌

#작성된 게시글 삭제
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id=%s", (id,)) #sql에서 삭제
    conn.commit() #반영
    conn.close()
    return redirect(url_for("index"))

#게시글 검색하기
@app.route("/search")
def search():
    q = request.args.get("q", "") #검색어 가져오기
    field = request.args.get("field", "all")  # 기본값은 전체 검색임

    conn = get_conn()
    cur = conn.cursor()

    if field == "title":
        cur.execute("SELECT * FROM posts WHERE title LIKE %s ORDER BY id DESC", (f"%{q}%",)) #제목으로 검색
    elif field == "content":
        cur.execute("SELECT * FROM posts WHERE content LIKE %s ORDER BY id DESC", (f"%{q}%",)) #내용으로 검색
    else:  # 전체 검색
        cur.execute(
            "SELECT * FROM posts WHERE title LIKE %s OR content LIKE %s ORDER BY id DESC",
            (f"%{q}%", f"%{q}%")
        )

    posts = cur.fetchall()
    conn.close()
    return render_template("index.html", posts=posts) #검색 결과 index

#상세 보기
@app.route("/post/<int:id>")
def detail(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id=%s", (id,)) #해당하는 게시글 불러옴
    post = cur.fetchone()
    conn.close()
    return render_template("detail.html", post=post) #상세 페이지로 이동

#flask 서버 실행
if __name__ == "__main__":
    app.run(debug=True)

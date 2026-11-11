# Bookly — MySQL + Flask classroom app

## 요구 사항
- Python 3.10 이상
- 로컬에서 실행 중인 MySQL Server 8.x (MySQL Workbench는 이 서버에 접속하기 위한 클라이언트 도구입니다.)

## 설정 방법
1. 해당 폴더에서 터미널을 엽니다.
2. 필요한 패키지를 설치합니다: `python -m pip install -r requirements.txt`
3. `.env.example` 파일을 `.env`라는 이름으로 복사하고, 본인의 로컬 MySQL 사용자 이름과 비밀번호를 입력합니다.
4. 애플리케이션을 실행합니다: `python app.py`
5. 웹 브라우저에서 http://127.0.0.1:5000 에 접속합니다.

이 애플리케이션은 `book_review` 데이터베이스와 그 안의 4개 테이블이 존재하지 않을 경우 자동으로 생성합니다. 또한, 테이블이 비어 있는 경우에만 데모용 사용자 및 도서 데이터를 추가합니다. **기존 데이터는 삭제하지 않습니다.** 만약 테이블이 이미 존재하지만 스키마가 다른 경우, MySQL Workbench를 사용하여 먼저 스키마를 조정해야 합니다. 데이터베이스를 생성하려면 `CREATE` 권한이 필요합니다. 또는, 애플리케이션을 실행하기 전에 MySQL Workbench에서 직접 `book_review` 데이터베이스를 생성해 두어도 됩니다.

## MySQL Workbench에서 확인하기
```sql
USE book_review;
SELECT * FROM users;
SELECT * FROM books;
SELECT * FROM reviews ORDER BY created_at DESC, id DESC;
SELECT * FROM favorites;
```

## 실습 과제
1. `home()` 함수 내의 SELECT 쿼리를 찾아 `ORDER BY b.created_at DESC, b.id DESC` 부분을 `ORDER BY b.title ASC`로 변경해 보세요.
2. 웹 브라우저를 통해 리뷰를 작성한 후, MySQL Workbench에서 `reviews` 테이블의 내용을 확인해 보세요.
3. `book_detail()` 함수 내에서 `reviews` 테이블과 `users` 테이블이 어떻게 JOIN(결합)되는지 확인해 보세요.
4. 즐겨찾기를 추가하거나 삭제해 보고, `favorites` 테이블의 변화를 확인해 보세요.

## 참고 사항
- 본 애플리케이션은 교육용 데모이며, 실제 서비스(운영 환경)용이 아닙니다.
- 사용자 선택 기능은 계정 시스템을 모사한 것으로, 실제 로그인이나 비밀번호 검증 과정은 포함되어 있지 않습니다.
- 데모 데이터에 포함된 `password` 값은 실제 비밀번호가 아닙니다. 실제 애플리케이션 개발 시 비밀번호를 평문(plain text)으로 저장하지 마십시오.
- `.env` 파일은 절대 공유하거나 Git에 커밋하지 마십시오.
- Flask의 디버그 모드는 로컬 개발 환경에서만 사용해야 합니다.
- CSS에는 Google Fonts가 포함되어 있으나, 인터넷 연결이 없는 오프라인 환경에서는 시스템 폰트가 적용됩니다.

---

## Requirements
- Python 3.10+
- MySQL Server 8.x running locally (MySQL Workbench is a client for this server)

## Setup
1. Open a terminal in this folder.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and enter your local MySQL username/password.
4. Run: `python app.py`
5. Open http://127.0.0.1:5000

The app creates `book_review` and its four tables if missing. It seeds demo users and books only if their tables are empty. **It does not delete existing data.** If the tables already exist with a different schema, adjust them in MySQL Workbench first. Creating the database requires CREATE privileges; alternatively, create `book_review` in Workbench before running the app.

## Inspect in MySQL Workbench
```sql
USE book_review;
SELECT * FROM users;
SELECT * FROM books;
SELECT * FROM reviews ORDER BY created_at DESC, id DESC;
SELECT * FROM favorites;
```

## Student tasks
1. Find the SELECT query in `home()` and change `ORDER BY b.created_at DESC, b.id DESC` to `ORDER BY b.title ASC`.
2. Submit a review in the browser, then inspect `reviews` in Workbench.
3. Identify the JOIN between `reviews` and `users` in `book_detail()`.
4. Add/remove a favorite and inspect the `favorites` table.

## Notes
- This is a local-only teaching demo, not a production app.
- The user selector simulates accounts; there is no login/password verification.
- Demo `password` values are not real passwords. Never store plaintext passwords in real applications.
- Do not share `.env` or commit it to Git.
- Flask debug mode is for local development only.
- CSS uses an optional Google Fonts import; system fonts work offline.

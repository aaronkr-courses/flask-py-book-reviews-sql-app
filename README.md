# Bookly — MySQL + Flask classroom app

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

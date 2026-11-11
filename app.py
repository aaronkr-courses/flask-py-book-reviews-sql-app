"""Classroom book-review application backed by MySQL Server."""
import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from mysql.connector import Error, errorcode

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'classroom-only-change-this')
DB_NAME = os.getenv('MYSQL_DATABASE', 'book_review')
if not DB_NAME.replace('_', '').isalnum() or not DB_NAME[0].isalpha():
    raise ValueError('MYSQL_DATABASE must contain only letters, numbers, and underscores and start with a letter.')

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'charset': 'utf8mb4',
}

@contextmanager
def database():
    conn = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(sql, params=()):
    with database() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()


def fetch_one(sql, params=()):
    with database() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            return cursor.fetchone()
        finally:
            cursor.close()


def execute(sql, params=()):
    with database() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()


def initialize():
    """Create missing database/tables and add demo records only to empty tables."""
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        cursor = conn.cursor()
        # 데이터베이스 생성하고 사용
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        cursor.execute(f'USE `{DB_NAME}`')

        # users 테이블 생성
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            ...
        ) ENGINE=InnoDB''')

        # books 테이블 생성
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            ...
        ) ENGINE=InnoDB''')

        # reviews 테이블 생성
        cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
            ...
        ) ENGINE=InnoDB''')

        # favorites 테이블 생성
        cursor.execute('''CREATE TABLE IF NOT EXISTS favorites (
            ...
        ) ENGINE=InnoDB''')

        # users 조회
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            # users 데이터 없으면 추가
            cursor.executemany('INSERT INTO users(username,password,bio) VALUES (%s,%s,%s)', [
                ('kim', 'demo-only-no-login', '독서를 좋아합니다.'),
                ('lee', 'demo-only-no-login', '소설을 좋아합니다.'),
                ('park', 'demo-only-no-login', '새로운 책을 찾고 있습니다.')
            ])

        # books 조회
        cursor.execute('SELECT COUNT(*) FROM books')
        if cursor.fetchone()[0] == 0:
            # books 데이터 없으면 추가
            cursor.executemany('INSERT INTO books(title) VALUES (%s)', [
                ('데이터베이스 입문',), ('SQL 기초',), ('프로그래밍의 이해',),
                ('웹 개발 첫걸음',), ('파이썬으로 시작하기',), ('데이터 모델링 연습',)
            ])
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.context_processor
def shared_context():
    users = fetch_all('SELECT id, username FROM users ORDER BY id')
    selected_id = session.get('user_id')
    if not any(user['id'] == selected_id for user in users):
        selected_id = users[0]['id'] if users else None
        session['user_id'] = selected_id
    current_user = next((u for u in users if u['id'] == selected_id), None)
    return {'users': users, 'current_user': current_user}


def current_user_id():
    user_id = session.get('user_id')
    if user_id is None:
        user = fetch_one('SELECT id FROM users ORDER BY id LIMIT 1')
        if user is None:
            abort(400, 'No demo users found')
        user_id = user['id']
        session['user_id'] = user_id
    return user_id


@app.post('/switch-user') # 사용자 변경
def switch_user():
    try:
        user_id = int(request.form.get('user_id', ''))
    except ValueError:
        abort(400)
    if not fetch_one('SELECT id FROM users WHERE id = %s', (user_id,)):
        abort(404)
    session['user_id'] = user_id
    return redirect(url_for('home'))


@app.get('/') # 홈페이지
def home():
    user_id = current_user_id()
    query = request.args.get('q', '').strip()[:100]
    # 홈페이지 데이터 조회
    books = fetch_all('''
        ...
    ''', (user_id, '%' + query + '%'))
    return render_template('index.html', books=books, query=query, page='home', heading='책을 발견하고, 생각을 나누세요', subtitle='읽고 싶은 책을 찾고 리뷰를 남겨보세요.')


@app.get('/favorites')
def favorites():
    # 즐겨찾기 데이터 조회
    books = fetch_all('''
        ...
    ''', (current_user_id(),))
    return render_template('index.html', books=books, query='', page='favorites', heading='나의 즐겨찾기', subtitle='다시 읽고 싶은 책을 한곳에서 확인하세요.')


@app.get('/book/<int:book_id>')
def book_detail(book_id):
    # 책 한권의 데이터 조회
    book = fetch_one('''
        SELECT b.id, b.title, b.created_at,
               EXISTS(SELECT 1 FROM favorites f WHERE f.book_id=b.id AND f.user_id=%s) AS is_favorite
        FROM books b WHERE b.id=%s
    ''', (current_user_id(), book_id))
    if book is None:
        abort(404)
    # 모든 리뷰 데이터 조회
    reviews = fetch_all('''
        SELECT r.id, r.content, r.created_at, u.username
        FROM reviews r JOIN users u ON r.user_id = u.id
        WHERE r.book_id = %s
        ORDER BY r.created_at DESC, r.id DESC
    ''', (book_id,))
    return render_template('book.html', book=book, reviews=reviews, page='book')


@app.post('/review/<int:book_id>')
def add_review(book_id):
    if not fetch_one('SELECT id FROM books WHERE id=%s', (book_id,)):
        abort(404)
    content = request.form.get('content', '').strip()
    if not 1 <= len(content) <= 2000:
        flash('리뷰는 1~2000자로 입력해주세요.', 'error')
    else:
        execute('INSERT INTO reviews(user_id, book_id, content) VALUES (%s, %s, %s)',
                (current_user_id(), book_id, content))
        flash('리뷰가 등록되었습니다.', 'success')
    return redirect(url_for('book_detail', book_id=book_id))


@app.post('/favorite/<int:book_id>')
def toggle_favorite(book_id):
    if not fetch_one('SELECT id FROM books WHERE id=%s', (book_id,)):
        abort(404)
    user_id = current_user_id()
    existing = fetch_one('SELECT id FROM favorites WHERE user_id=%s AND book_id=%s', (user_id, book_id))
    if existing:
        execute('DELETE FROM favorites WHERE user_id=%s AND book_id=%s', (user_id, book_id))
        flash('즐겨찾기에서 제거했습니다.', 'success')
    else:
        try:
            execute('INSERT INTO favorites(user_id, book_id) VALUES (%s, %s)', (user_id, book_id))
        except mysql.connector.IntegrityError as exc:
            if exc.errno != errorcode.ER_DUP_ENTRY:
                raise
        flash('즐겨찾기에 추가했습니다.', 'success')
    return redirect(url_for('book_detail', book_id=book_id))


@app.post('/books')
def add_book():
    title = request.form.get('title', '').strip()
    if not 1 <= len(title) <= 255:
        flash('책 제목은 1~255자로 입력해주세요.', 'error')
    else:
        execute('INSERT INTO books(title) VALUES (%s)', (title,))
        flash('새 책이 등록되었습니다.', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    try:
        initialize()
    except Error as exc:
        raise SystemExit(f'MySQL connection/setup failed: {exc}\nCheck MySQL Server, .env credentials, and CREATE DATABASE permissions.')
    app.run(host='127.0.0.1', port=5000, debug=True)

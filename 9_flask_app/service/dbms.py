from werkzeug.security import generate_password_hash
import sqlite3
from models.user import User


__conn = sqlite3.connect("../9_flask_app/database.db", check_same_thread=False)
__cur = __conn.cursor()
__exe = __cur.execute
__scr = __cur.executescript
__com = __conn.commit
__one = __cur.fetchone
__all = __cur.fetchall


def get_one_user(login: str) -> User:
    __exe("SELECT * FROM users WHERE login = ?", (login,))
    result = __one()
    return User(*result) if result is not None else None


def add_user(user: User) -> bool:
    __exe("SELECT * FROM users WHERE login = ?", (user.login,))
    if __one() is not None:
        return False
    hash_password = generate_password_hash(user.hash_password, 'sha256', 64)
    user.hash_password = hash_password
    user.salt = hash_password.split('$')[1]
    __exe("INSERT INTO users (login, hash_password, salt, date_registration) VALUES (?, ?, ?, ?)",
          user.get_tuple())
    __com()
    return True


def update_user(old_login: str, updatable_user: User) -> bool:
    __exe("SELECT * FROM users WHERE login = ?", (old_login,))
    if __one() is None:
        return False
    hash_password = generate_password_hash(updatable_user.hash_password, 'sha256', 64)
    updatable_user.hash_password = hash_password
    updatable_user.salt = hash_password.split('$')[1]
    __exe("UPDATE users SET login = ?, hash_password =?, salt = ?, date_registration = ? WHERE login = ?",
          (*updatable_user.get_tuple(), old_login))
    __com()
    return True


def delete_user(user: User) -> bool:
    __exe("SELECT * FROM users WHERE login = ?", (user.login,))
    if __one() is None:
        return False
    __exe("DELETE FROM users WHERE login = ?", (user.login,))
    __com()
    return True
from unittest import TestCase

from models.users.user import User
from models.testware import get_test_connection, reset_database


class TestUser(TestCase):
    def test_crud(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        # Get nonexistent
        user = User.get_user(cur, 0)
        assert user is None  # Get where user doesn't exist returns None

        # Create user
        user_id = User.create_user(
            cur, User(user_id=None, username='username', pin='1234', user_type_id=1,
                      created_at=None, updated_at=None, deleted=None))
        assert user_id is not None  # ID was present
        assert user_id != 0  # ID was something sensible

        # Get user
        user = User.get_user(cur, user_id)
        assert user.id == user_id  # ID was set
        assert user.pin == '1234'  # Pin name was set

        # Update user
        user.pin = '5678'
        User.update_user(cur, user)
        user = User.get_user(cur, user_id)
        assert user.pin == '5678'  # First name was updated

        # Delete user
        User.delete_user(cur, user_id)
        user = User.get_user(cur, user_id)
        assert user is None  # None is returned when deleted is true

        # Double-check that row still exists with manual query
        cur.execute('SELECT * FROM users WHERE id=%s', (user_id,))
        assert cur.rowcount == 1  # Ensure we got a row
        user = User.user_from_tuple(cur.fetchone())
        assert user.deleted  # Make sure row still exists, and deleted is true

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

    def test_attempt_login(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        # Create children
        user_id = User.create_user(
            cur, User(user_id=None, username='username', pin='1234', user_type_id=1,
                      created_at=None, updated_at=None, deleted=None))

        user = User.attempt_login(cur, 'bad_username', '1234')  # Test wrong name
        assert user is None

        user = User.attempt_login(cur, 'username', '0000')  # Test wrong pin
        assert user is None

        user = User.attempt_login(cur, 'username', '1234')  # Test correct creds
        assert user is not None

        conn.commit()

        pass
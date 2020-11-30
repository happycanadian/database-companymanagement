from unittest import TestCase

from models.users.user_type import UserType
from models.testware import get_test_connection, reset_database


class TestUserType(TestCase):
    def test_get_all(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        user_types = UserType.get_all_user_types(cur)
        assert user_types is not None  # Ensure something was returned
        assert len(user_types) > 1  # Ensure multiple types were returned

        conn.commit()
        pass

    def test_get(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        user_type = UserType.get_user_type(cur, 0)
        assert user_type is None  # Ensure none was returned for bad ID
        user_type = UserType.get_user_type(cur, 1)
        assert user_type is not None  # Ensure something was returned for valid ID
        assert user_type.id == 1  # Ensure correct type was returned

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

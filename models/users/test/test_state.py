from unittest import TestCase

from models.users.state import State
from models.testware import get_test_connection, reset_database


class TestState(TestCase):
    def test_get_all(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        states = State.get_all_states(cur)
        assert states is not None  # Ensure something was returned
        assert len(states) > 1  # Ensure multiple types were returned

        conn.commit()
        pass

    def test_get(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        state = State.get_state(cur, 0)
        assert state is None  # Ensure none was returned for bad ID
        state = State.get_state(cur, 1)
        assert state is not None  # Ensure something was returned for valid ID
        assert state.id == 1  # Ensure correct type was returned

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

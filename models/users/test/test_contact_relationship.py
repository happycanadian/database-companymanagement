from unittest import TestCase

from models.users.contact_relationship import ContactRelationship
from models.testware import get_test_connection, reset_database


class TestContactRelationship(TestCase):
    def test_get_all(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        contact_relationships = ContactRelationship.get_all_contact_relationships(cur)
        assert contact_relationships is not None  # Ensure something was returned
        assert len(contact_relationships) > 1  # Ensure multiple types were returned

        conn.commit()
        pass

    def test_get(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        contact_relationship = ContactRelationship.get_contact_relationship(cur, 0)
        assert contact_relationship is None  # Ensure none was returned for bad ID
        contact_relationship = ContactRelationship.get_contact_relationship(cur, 1)
        assert contact_relationship is not None  # Ensure something was returned for valid ID
        assert contact_relationship.id == 1  # Ensure correct type was returned

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

    pass

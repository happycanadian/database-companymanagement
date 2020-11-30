from unittest import TestCase

from models.users.address import Address
from models.users.contact_information import ContactInformation
from models.testware import reset_database, get_test_connection


class TestContactInformation(TestCase):
    def test_crud(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        # Create children
        address_id = Address.create_address(
            cur, Address(address_id=None, street='1st street', city='city', states_id=1, postal_code='55555',
                         country_abbreviation='US', created_at=None, updated_at=None, deleted=None))

        # Get nonexistent
        contact_information = ContactInformation.get_contact_information(cur, 0)
        assert contact_information is None  # Get where contact information doesn't exist returns None

        # Create contact information
        contact_information_id = ContactInformation.create_contact_information(cur, ContactInformation(
            contact_information_id=None, email='test@email.com', phone_number='+15555555555', address_id=address_id,
            created_at=None, updated_at=None, deleted=None))
        assert contact_information_id is not None  # ID was present
        assert contact_information_id != 0  # ID was something sensible

        # Get contact information
        contact_information = ContactInformation.get_contact_information(cur, contact_information_id)
        assert contact_information.id == contact_information_id  # ID was set
        assert contact_information.phone_number == '+15555555555'  # Phone number was set

        # Update contact information
        contact_information.phone_number = '+16085555555'
        ContactInformation.update_contact_information(cur, contact_information)
        contact_information = ContactInformation.get_contact_information(cur, contact_information_id)
        assert contact_information.phone_number == '+16085555555'  # Phone number was updated

        # Delete contact information
        ContactInformation.delete_contact_information(cur, contact_information_id)
        contact_information = ContactInformation.get_contact_information(cur, contact_information_id)
        assert contact_information is None  # None is returned when deleted is true

        # Double-check that row still exists with manual query
        cur.execute('SELECT * FROM contact_information WHERE id=%s', (contact_information_id,))
        assert cur.rowcount == 1  # Ensure we got a row
        contact_information = ContactInformation.contact_information_from_tuple(cur.fetchone())
        assert contact_information.deleted  # Make sure row still exists, and deleted is true

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

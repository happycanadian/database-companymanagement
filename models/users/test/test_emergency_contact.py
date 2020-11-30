from unittest import TestCase

from models.users.address import Address
from models.users.emergency_contact import EmergencyContact
from models.testware import get_test_connection, reset_database


class TestEmergencyContact(TestCase):
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
        emergency_contact = EmergencyContact.get_emergency_contact(cur, 0)
        assert emergency_contact is None  # Get where emergency contact doesn't exist returns None

        # Create emergency contact
        emergency_contact_id = EmergencyContact.create_emergency_contact(
            cur, EmergencyContact(emergency_contact_id=None, first_name='First', last_name='Last',
                                  contact_relationship_id=1, email='test@email.com', phone_number='+15555555555',
                                  address_id=address_id, created_at=None, updated_at=None, deleted=None))
        assert emergency_contact_id is not None  # ID was present
        assert emergency_contact_id != 0  # ID was something sensible

        # Get emergency contact
        emergency_contact = EmergencyContact.get_emergency_contact(cur, emergency_contact_id)
        assert emergency_contact.id == emergency_contact_id  # ID was set
        assert emergency_contact.phone_number == '+15555555555'  # Phone number was set

        # Update emergency contact
        emergency_contact.phone_number = '+16085555555'
        EmergencyContact.update_emergency_contact(cur, emergency_contact)
        contact_information = EmergencyContact.get_emergency_contact(cur, emergency_contact_id)
        assert contact_information.phone_number == '+16085555555'  # Phone number was updated

        # Delete contact information
        EmergencyContact.delete_emergency_contact(cur, emergency_contact_id)
        contact_information = EmergencyContact.get_emergency_contact(cur, emergency_contact_id)
        assert contact_information is None  # None is returned when deleted is true

        # Double-check that row still exists with manual query
        cur.execute('SELECT * FROM emergency_contacts WHERE id=%s', (emergency_contact_id,))
        assert cur.rowcount == 1  # Ensure we got a row
        contact_information = EmergencyContact.emergency_contact_from_tuple(cur.fetchone())
        assert contact_information.deleted  # Make sure row still exists, and deleted is true

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

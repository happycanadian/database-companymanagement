from unittest import TestCase

from psycopg2._psycopg import Date

from models.users.address import Address
from models.users.contact_information import ContactInformation
from models.users.emergency_contact import EmergencyContact
from models.users.user_data import UserData
from models.testware import get_test_connection, reset_database


class TestUserData(TestCase):
    def test_crud(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        # Create children
        contact_information_address_id = Address.create_address(
            cur, Address(address_id=None, street='1st street', city='city', states_id=1, postal_code='55555',
                         country_abbreviation='US', created_at=None, updated_at=None, deleted=None))
        contact_information_id = ContactInformation.create_contact_information(cur, ContactInformation(
            contact_information_id=None, email='test@email.com', phone_number='+15555555555',
            address_id=contact_information_address_id,
            created_at=None, updated_at=None, deleted=None))
        emergency_contact_address_id = Address.create_address(
            cur, Address(address_id=None, street='1st street', city='city', states_id=1, postal_code='55555',
                         country_abbreviation='US', created_at=None, updated_at=None, deleted=None))
        emergency_contact_id = EmergencyContact.create_emergency_contact(
            cur, EmergencyContact(emergency_contact_id=None, first_name='First', last_name='Last',
                                  contact_relationship_id=1, email='test@email.com', phone_number='+15555555555',
                                  address_id=emergency_contact_address_id, created_at=None, updated_at=None,
                                  deleted=None))

        # Get nonexistent
        user_data = UserData.get_user_data(cur, 0)
        assert user_data is None  # Get where user data doesn't exist returns None

        # Create user data
        user_data_id = UserData.create_user_data(
            cur, UserData(user_data_id=None, first_name='first', last_name='last', date_of_birth=Date(1998, 1, 10),
                          contact_information_id=contact_information_id, emergency_contact_id=emergency_contact_id,
                          created_at=None, updated_at=None, deleted=None))
        assert user_data_id is not None  # ID was present
        assert user_data_id != 0  # ID was something sensible

        # Get user data
        user_data = UserData.get_user_data(cur, user_data_id)
        assert user_data.id == user_data_id  # ID was set
        assert user_data.first_name == 'first'  # First name was set

        # Update user data
        user_data.first_name = 'second'
        UserData.update_user_data(cur, user_data)
        user_data = UserData.get_user_data(cur, user_data_id)
        assert user_data.first_name == 'second'  # First name was updated

        # Delete user data
        UserData.delete_user_data(cur, user_data_id)
        user_data = UserData.get_user_data(cur, user_data_id)
        assert user_data is None  # None is returned when deleted is true

        # Double-check that row still exists with manual query
        cur.execute('SELECT * FROM user_data WHERE id=%s', (user_data_id,))
        assert cur.rowcount == 1  # Ensure we got a row
        user_data = UserData.user_data_from_tuple(cur.fetchone())
        assert user_data.deleted  # Make sure row still exists, and deleted is true

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

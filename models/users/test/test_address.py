from unittest import TestCase

from models.users.address import Address
from models.testware import reset_database, get_test_connection


class TestAddress(TestCase):
    def test_crud(self):
        # Setup
        conn = get_test_connection()
        reset_database(conn)
        cur = conn.cursor()

        # Get nonexistent
        address = Address.get_address(cur, 0)
        assert address is None  # Get where address doesn't exist returns None

        # Create address
        address_id = Address.create_address(
            cur, Address(address_id=None, street='1st street', city='city', states_id=1, postal_code='55555',
                         country_abbreviation='US', created_at=None, updated_at=None, deleted=None))
        assert address_id is not None  # ID was present
        assert address_id != 0  # ID was something sensible

        # Get address
        address = Address.get_address(cur, address_id)
        assert address.id == address_id  # ID was set
        assert address.street == '1st street'  # Street was set

        # Update address
        address.street = '2nd street'
        Address.update_address(cur, address)
        address = Address.get_address(cur, address_id)
        assert address.street == '2nd street'  # Street was updated

        # Delete address
        Address.delete_address(cur, address_id)
        address = Address.get_address(cur, address_id)
        assert address is None  # None is returned when deleted is true

        # Double-check that row still exists with manual query
        cur.execute('SELECT * FROM addresses WHERE id=%s', (address_id,))
        assert cur.rowcount == 1  # Ensure we got a row
        address = Address.address_from_tuple(cur.fetchone())
        assert address.deleted  # Make sure row still exists, and deleted is true

        # Ensure we can commit without violating constraints
        conn.commit()

        pass

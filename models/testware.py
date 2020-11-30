import psycopg2
from psycopg2._psycopg import Date

from models.users.address import Address
from models.users.contact_information import ContactInformation
from models.users.emergency_contact import EmergencyContact
from models.users.user import User
from models.users.user_data import UserData


def reset_database(conn):
    cur = conn.cursor()
    cur.execute('DELETE FROM shifts CASCADE')
    cur.execute('DELETE FROM shift_roles CASCADE')
    cur.execute('DELETE FROM roles CASCADE')
    cur.execute('DELETE FROM staff CASCADE')
    cur.execute('DELETE FROM users CASCADE')
    cur.execute('DELETE FROM user_data CASCADE')
    cur.execute('DELETE FROM contact_information CASCADE')
    cur.execute('DELETE FROM emergency_contacts CASCADE')
    cur.execute('DELETE FROM addresses CASCADE')
    cur.execute('DELETE FROM jobs CASCADE')
    cur.execute('DELETE FROM buildings CASCADE')
    conn.commit()


def get_test_connection():
    # conn = psycopg2.connect("dbname=db user=postgres password=Troll321")
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Troll321")
    conn.set_session(deferrable=True)
    return conn


def make_test_user(conn):
    cur = conn.cursor()
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
    user_data_id = UserData.create_user_data(
        cur, UserData(user_data_id=None, first_name='first', last_name='last', date_of_birth=Date(1998, 1, 10),
                      contact_information_id=contact_information_id, emergency_contact_id=emergency_contact_id,
                      created_at=None, updated_at=None, deleted=None))
    user_id = User.create_user(
        cur, User(user_id=None, username='username', pin='1234', user_type_id=1, user_data_id=user_data_id,
                  created_at=None, updated_at=None, deleted=None))
    conn.commit()
    return user_id

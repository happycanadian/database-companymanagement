import psycopg2

from models.users.contact_information import ContactInformation
from models.testware import reset_database, get_test_connection

if __name__ == '__main__':
    conn = get_test_connection()

    # print(map(lambda user: str(user), User.get_all_users(conn.cursor())))
    # print(UserData.get_user_data(conn.cursor(), 1))
    # print(ContactInformation.get_contact_information(conn.cursor(), 1))
    # print(EmergencyContact.get_emergency_contact(conn.cursor(), 1))
    # print(Address.get_address(conn.cursor(), 1))
    # print(map(lambda state: str(state), State.get_all_states(conn.cursor())))
    # print(map(lambda contact_relationship: str(contact_relationship),
    #           ContactRelationship.get_all_contact_relationships(conn.cursor())))

    #reset_database(conn)

    cur = conn.cursor()
    contact_information_id = ContactInformation.create_contact_information(cur, ContactInformation(
        contact_information_id=None, email='test@email.com', phone_number='+15555555555', address_id=1,
        created_at=None, updated_at=None, deleted=None))
    print(contact_information_id)
    conn.commit()

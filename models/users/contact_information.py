from models.auditable import AuditableEntity


class ContactInformation(AuditableEntity):
    def __init__(self, contact_information_id, email, phone_number, address_id, created_at, updated_at, deleted):
        AuditableEntity.__init__(self, contact_information_id, created_at, updated_at, deleted)
        self.email = email
        self.phone_number = phone_number
        self.address_id = address_id

    def __str__(self):
        return 'ContactInformation{id=% s, email=% s, phone_number=% s, address_id=% s}' \
               % (self.id, self.email, self.phone_number, self.address_id)

    @staticmethod
    def get_contact_information(cur, contact_information_id):
        cur.execute('SELECT * FROM contact_information WHERE id=%s AND deleted IS FALSE', (contact_information_id,))
        row = cur.fetchone()
        return None if cur.rowcount == 0 else ContactInformation.contact_information_from_tuple(row)

    @staticmethod
    def create_contact_information(cur, contact_information):
        cur.execute(
            'INSERT INTO contact_information (email, phone_number, address_id)'
            ' VALUES (%s, %s, %s) RETURNING contact_information.id',
            (contact_information.email, contact_information.phone_number, contact_information.address_id))
        return cur.fetchone()[0]

    @staticmethod
    def update_contact_information(cur, contact_information):
        cur.execute(
            'UPDATE contact_information SET email = %s, phone_number = %s, address_id = %s'
            ' WHERE id = %s',
            (contact_information.email, contact_information.phone_number, contact_information.address_id, contact_information.id))

    @staticmethod
    def delete_contact_information(cur, contact_information_id):
        cur.execute(
            'UPDATE contact_information SET deleted = TRUE WHERE id = %s',
            (contact_information_id,))

    @staticmethod
    def contact_information_from_tuple(contact_information_tuple):
        contact_information_id, email, phone_number, address_id, created_at, updated_at, deleted = \
            contact_information_tuple
        return ContactInformation(contact_information_id, email, phone_number, address_id, created_at, updated_at,
                                  deleted)

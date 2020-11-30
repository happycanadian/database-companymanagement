from models.auditable import AuditableEntity


class EmergencyContact(AuditableEntity):
    def __init__(self, emergency_contact_id, first_name, last_name, contact_relationship_id, email, phone_number,
                 address_id, created_at, updated_at, deleted):
        AuditableEntity.__init__(self, emergency_contact_id, created_at, updated_at, deleted)
        self.first_name = first_name
        self.last_name = last_name
        self.contact_relationship_id = contact_relationship_id
        self.email = email
        self.phone_number = phone_number
        self.address_id = address_id

    def __str__(self):
        return 'EmergencyContact{id=% s, first_name=% s, last_name=% s, contact_relationship_id=% s, email=% s, ' \
               'phone_number=% s, address_id=% s}' % (
                   self.id, self.first_name, self.last_name, self.contact_relationship_id, self.email,
                   self.phone_number, self.address_id)

    @staticmethod
    def get_emergency_contact(cur, emergency_contact_id):
        cur.execute(
            'SELECT * FROM emergency_contacts WHERE id=%s AND NOT deleted',
            (emergency_contact_id,))
        return None if cur.rowcount == 0 else EmergencyContact.emergency_contact_from_tuple(cur.fetchone())

    @staticmethod
    def create_emergency_contact(cur, emergency_contact):
        cur.execute(
            'INSERT INTO emergency_contacts (first_name, last_name, contact_relationship_id, email, phone_number,'
            ' address_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (emergency_contact.first_name, emergency_contact.last_name, emergency_contact.contact_relationship_id,
             emergency_contact.email, emergency_contact.phone_number, emergency_contact.address_id))
        return cur.fetchone()[0]

    @staticmethod
    def update_emergency_contact(cur, emergency_contact):
        cur.execute(
            'UPDATE emergency_contacts SET first_name = %s, last_name = %s, contact_relationship_id = %s, email = %s, '
            'phone_number = %s, address_id = %s WHERE id = %s',
            (emergency_contact.first_name, emergency_contact.last_name, emergency_contact.contact_relationship_id,
             emergency_contact.email, emergency_contact.phone_number, emergency_contact.address_id,
             emergency_contact.id))

    @staticmethod
    def delete_emergency_contact(cur, emergency_contact_id):
        cur.execute('UPDATE emergency_contacts SET deleted = TRUE WHERE id = %s', (emergency_contact_id,))

    @staticmethod
    def emergency_contact_from_tuple(emergency_contact_tuple):
        emergency_contact_id, first_name, last_name, contact_relationship_id, email, phone_number, \
        address_id, created_at, updated_at, deleted = emergency_contact_tuple
        return EmergencyContact(emergency_contact_id, first_name, last_name, contact_relationship_id, email,
                                phone_number, address_id, created_at, updated_at, deleted)

from models.auditable import AuditableEntity


class ContactRelationship(AuditableEntity):
    def __init__(self, contact_relationship_id, contact_relationship_type, created_at, updated_at, deleted):
        AuditableEntity.__init__(self, contact_relationship_id, created_at, updated_at, deleted)
        self.type = contact_relationship_type

    def __str__(self):
        return 'ContactRelationships{id=% s, contact_relationship_type=% s}' % (self.id, self.type)

    @staticmethod
    def get_all_contact_relationships(cur):
        cur.execute('SELECT * FROM contact_relationships')
        return None if cur.rowcount == 0 else map(ContactRelationship.contact_relationship_from_tuple, cur.fetchall())

    @staticmethod
    def get_contact_relationship(cur, contact_relationship_id):
        cur.execute('SELECT * FROM contact_relationships WHERE id = %s', (contact_relationship_id,))
        return None if cur.rowcount == 0 else ContactRelationship.contact_relationship_from_tuple(cur.fetchone())

    @staticmethod
    def contact_relationship_from_tuple(contact_relationship_tuple):
        contact_relationship_id, contact_relationship_type, created_at, updated_at, deleted = contact_relationship_tuple
        return ContactRelationship(contact_relationship_id, contact_relationship_type, created_at, updated_at, deleted)
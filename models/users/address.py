from models.auditable import AuditableEntity


class Address(AuditableEntity):
    def __init__(self, address_id, street, city, states_id, postal_code, country_abbreviation, created_at, updated_at,
                 deleted):
        AuditableEntity.__init__(self, address_id, created_at, updated_at, deleted)
        self.street = street
        self.city = city
        self.states_id = states_id
        self.postal_code = postal_code
        self.country_abbreviation = country_abbreviation

    def __str__(self):
        return 'Address{id=% s, street=% s, city=% s, states_id=% s, postal_code=% s, country_abbreviation=% s}' % \
               (self.id, self.street, self.city, self.states_id, self.postal_code, self.country_abbreviation)

    @staticmethod
    def get_address(cur, address_id):
        cur.execute('SELECT * FROM addresses WHERE addresses.id=%s AND NOT addresses.deleted', (address_id,))
        return None if cur.rowcount == 0 else Address.address_from_tuple(cur.fetchone())

    @staticmethod
    def create_address(cur, address):
        cur.execute('INSERT INTO addresses (street, city, states_id, postal_code, country_abbreviation)'
                    ' VALUES (%s, %s, %s, %s, %s) RETURNING addresses.id', (
                        address.street, address.city, address.states_id, address.postal_code,
                        address.country_abbreviation))
        return cur.fetchone()[0]

    @staticmethod
    def update_address(cur, address):
        cur.execute(
            'UPDATE addresses SET street = %s, city = %s, states_id = %s, postal_code = %s, country_abbreviation = %s'
            ' WHERE addresses.id=%s',
            (address.street, address.city, address.states_id, address.postal_code, address.country_abbreviation,
             address.id))

    @staticmethod
    def delete_address(cur, address_id):
        cur.execute('UPDATE addresses SET deleted=true WHERE addresses.id=%s', (address_id,))

    @staticmethod
    def address_from_tuple(address_tuple):
        address_id, street, city, states_id, postal_code, country_abbreviation, created_at, updated_at, deleted = \
            address_tuple
        return Address(address_id, street, city, states_id, postal_code, country_abbreviation, created_at, updated_at,
                       deleted)

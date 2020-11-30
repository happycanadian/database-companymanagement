from models.auditable import AuditableEntity


class State(AuditableEntity):
    def __init__(self, state_id, state_abbreviation, created_at, updated_at, deleted):
        AuditableEntity.__init__(self, state_id, created_at, updated_at, deleted)
        self.state_abbreviation = state_abbreviation

    def __str__(self):
        return 'State{id=% s, state_abbreviation=% s}' % (self.id, self.state_abbreviation)

    @staticmethod
    def get_all_states(cur):
        cur.execute('SELECT * FROM states WHERE NOT states.deleted')
        return None if cur.rowcount == 0 else map(State.state_from_tuple, cur.fetchall())

    @staticmethod
    def get_state(cur, state_id):
        cur.execute('SELECT * FROM states WHERE id = %s', (state_id,))
        return None if cur.rowcount == 0 else State.state_from_tuple(cur.fetchone())

    @staticmethod
    def state_from_tuple(state_tuple):
        state_id, state_abbreviation, created_at, updated_at, deleted = state_tuple
        return State(state_id, state_abbreviation, created_at, updated_at, deleted)
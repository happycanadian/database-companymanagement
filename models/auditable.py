class AuditableEntity(object):
    def __init__(self, auditable_entity_id, created_at, updated_at, deleted):
        self.id = auditable_entity_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted = deleted

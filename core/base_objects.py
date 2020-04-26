from core.world import world

class ObjectWithProcedures:
    def __init__(self):
        self.procedures = []

    def add_procedure(self, procedure, index=None):
        index = index or len(self.procedures)

        for policy in world.policies:
            procedure = policy.decorate_procedure(procedure)

        self.procedures.insert(index, procedure)

    def tick(self):
        for procedure in self.procedures:
            if procedure.should_apply(self):
                procedure.apply(self)



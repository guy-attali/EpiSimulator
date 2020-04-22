from procedures.base import Procedure

class DecoratedProcedure(Procedure):
  def __init__ (self, procedure):
    self.decorated_procedure = procedure

  def should_apply(self, person):
    return False

  def apply(self, person):
    return person


class Policy():

  def decorate_procedure (self, procedure):
    return procedure

  def world_pretick(self):
    pass
  
  def world_posttick(self):
    pass
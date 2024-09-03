from interface import Interface
from refresher import Refresher

def control_impl(data):
  
  return data

class Controller:
  @classmethod
  def run(cls, interface: Interface, refresher: Refresher):
    data = interface.run()
    postprocessed_data = cls.controll(data)
    refresher.run(postprocessed_data)
    
  @classmethod
  def controll(cls, data):
    return control_impl(data)
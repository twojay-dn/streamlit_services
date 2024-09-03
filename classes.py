from typing import Any, Dict

class Data:
  def __init__(self, d : Dict[str, Any] = None):
    self.data = d

  def get(self, key : str):
    return self.data[key]
  
  def set(self, key : str, value : Any, is_override : bool = False):
    if key in self.data and not is_override:
      raise ValueError(f"Key {key} already exists")
    self.data[key] = value

  def turnoff_all_boolean(self):
    for i in self.data:
      if isinstance(self.data[i], bool):
        self.data[i] = False

  def turnon_all_boolean(self):
    for i in self.data:
      if isinstance(self.data[i], bool):
        self.data[i] = True

  def __str__(self):
    return str(self.data)

  def __repr__(self):
    return str(self.data)

  def __getitem__(self, key):
    return self.data[key]
from controller import Controller
from interface import Interface
from refresher import Refresher

if __name__ == "__main__":
  Controller.run(interface=Interface, refresher=Refresher)
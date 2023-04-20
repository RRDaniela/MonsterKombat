from abc import ABC, abstractmethod
from settings import *
from monster import *

p1 = True
p2 = False

class MonsterFactory(ABC):
    @abstractmethod
    def crear_monstruo(self):
        pass

class MonsterFactoryHeavy(MonsterFactory):
    def crear_monstruo(self):
        return Monster(200, 370, False, 20, p1, DOSBRAZOS_DATA, dosBrazos_sheet, DOSBRAZOS_ANIMATION_STEPS)

class MonsterFactoryAgile(MonsterFactory):
    def crear_monstruo(self):
        return Monster(700, 370, True, 15, p2,  MDB_DATA, mdb_sheet, MDB_ANIMATION_STEPS)



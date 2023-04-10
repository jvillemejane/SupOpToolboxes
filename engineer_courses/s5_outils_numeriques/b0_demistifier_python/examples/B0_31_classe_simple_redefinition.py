#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Outils Numériques / Semestre 5 / Institut d'Optique

Classe simple / Redéfinition fonction __str__

Created on 09/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

class Animal:
	""" object class Animal
	"""	
	def __init__(self, name="Hello", sound="..."):
		""" Animal class constructor
		:name: name of the animal
		"""
		self.name = name
		self.sound = sound
		self.birthyear = 2000
		
	def __str__(self):
		""" Animal class display
		"""
		return f"Animal [ {self.name} ] born in {self.birthyear}"
		
	def move(self):
		print(f"\t[ {self.name} ] is moving")
		
	def speak(self):
		print(f"\t[ {self.name} ] is saying {self.sound}")
        
        

# Test of the class Animal
if __name__ == '__main__':
    animal1 = Animal()
    print("Animal 1 Name = ", animal1.name)
    animal2 = Animal("Garfield")
    print("Animal 2 Name = ", animal2.name)
    
    print(animal1)
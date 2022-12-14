# -*- coding: utf-8 -*-
"""
Object-Oriented Programming - First Exemple 

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-02
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

class Cat(Animal):
	""" Object class Cat, inherit from Animal
	"""
	def __init__(self, name="Hello", sound="Miaouh"):
		""" Cat class constructor
		:name: name of the animal
		"""
		super().__init__(name, sound)
		
	def __str__(self):
		""" Cat class display
		"""
		return f"Animal/CAT [ {self.name} ] born in {self.birthyear}"


class Dog(Animal):
	""" Object class Dog, inherit from Animal
	"""
	def __init__(self, name="Hello", sound="Wouaf"):
		""" Dog class constructor
		:name: name of the animal
		"""
		super().__init__(name, sound)
		
	def __str__(self):
		""" Dog class display
		"""
		return f"Animal/DOG [ {self.name} ] born in {self.birthyear}"		


# Test of the class Animal
if __name__ == '__main__':
	animal1 = Animal()
	print("Animal 1 Name = ", animal1.name)
	animal2 = Animal("Garfield")
	print("Animal 2 Name = ", animal2.name)

	print(animal2)
	animal2.move()
	animal2.speak()
	
	cat1 = Cat("Tigrou")
	print(cat1)
	cat1.move()
	cat1.speak()
	
	dog1 = Dog("Ralph")
	dog1.birthyear = 2012
	print(dog1)
	dog1.move()
	dog1.speak()
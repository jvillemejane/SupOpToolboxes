#include <iostream>
#include <string.h>

using namespace std;

class Animal
{
    public:
        char name[32];
        char sound[32];
        int birthyear;

        Animal() {     // Constructor
            strcpy(this->name, "Hello");
            strcpy(this->sound, "...");
            this->birthyear = 2000;
        }

        Animal(char name[]) {     // Constructor
            strcpy(this->name, name);
            strcpy(this->sound, "...");
            this->birthyear = 2000;
        }

        friend ostream &operator<<( ostream &output, const Animal a ) {
            output << "Animal [" << a.name << "] born in " << a.birthyear;
            return output;
        }

        void move(){
            cout << this->name << " is walking " << endl;
        }
        void speak(){
            cout << this->name << " is saying " << this->sound << endl;
        }
};

class Cat: public Animal{
    public :
        Cat(): Animal(){
            strcpy(this->sound, "Miaouh");
        }

        friend ostream &operator<<( ostream &output, const Cat a ) {
            output << "Animal/ CAT [" << a.name << "] born in " << a.birthyear;
            return output;
        }
};

class Dog: public Animal{
    public :
        Dog(): Animal(){
            strcpy(this->sound, "Waouf");
        }

        Dog(char name[]): Animal(name){
            strcpy(this->sound, "Waouf");
        }

        friend ostream &operator<<( ostream &output, const Dog a ) {
            output << "Animal/ DOG [" << a.name << "] born in " << a.birthyear;
            return output;
        }
};

/*
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


	cat1 = Cat("Tigrou")
	print(cat1)
	cat1.move()
	cat1.speak()

	dog1 = Dog("Ralph")
	dog1.birthyear = 2012
	print(dog1)
	dog1.move()
	dog1.speak()

*/



int main()
{
    cout << "Hello world!" << endl;

    int16_t     a = 20000;
    int16_t     b = a * a;
    cout << "a**2 = " << b << endl;

    cout << &a << endl;

    // Class testing

    Animal animal1;
    cout << "Animal 1 Name = " << animal1.name << endl;
    Animal animal2("Garfield");
    cout << "Animal 2 Name = " << animal2.name << endl;


    animal1.move();
    animal1.speak();

    cout << animal1 << endl;

    Cat cat1;
    cout << cat1 << endl;
    cat1.move();
	cat1.speak();

	Dog dog1("Ralph");
	dog1.birthyear = 2012;
    cout << dog1 << endl;
	dog1.move();
	dog1.speak();

    return 0;
}

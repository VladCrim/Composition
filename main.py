# 1. Создайте базовый класс `Animal`, который будет содержать общие атрибуты (например, `name`, `age`) и
# методы (`make_sound()`, `eat()`) для всех животных.
# # 2. Реализуйте наследование, создав подклассы `Bird`, `Mammal`, и `Reptile`, которые наследуют от класса `Animal`.
# Добавьте специфические атрибуты и переопределите методы, если требуется (например, различный звук для `make_sound()`).
# # 3. Продемонстрируйте полиморфизм: создайте функцию `animal_sound(animals)`, которая принимает список животных и
# вызывает метод `make_sound()` для каждого животного.
# # 4. Используйте композицию для создания класса `Zoo`, который будет содержать информацию о животных и сотрудниках.
# Должны быть методы для добавления животных и сотрудников в зоопарк.
# # 5. Создайте классы для сотрудников, например, `ZooKeeper`, `Veterinarian`, которые могут иметь специфические
# методы (например, `feed_animal()` для `ZooKeeper` и `heal_animal()` для `Veterinarian`).
# # Дополнительно:
# Попробуйте добавить дополнительные функции в вашу программу, такие как сохранение информации о зоопарке в файл и
# возможность её загрузки, чтобы у вашего зоопарка было "постоянное состояние" между запусками программы.

import json

class Animal:
    def __init__(self, name, age, color):
        self.name = name
        self.age = age
        self.color = color

    def make_sound(self):
        pass

    def eat(self):
        pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "age": self.age,
            "color": self.color
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"], data["color"])

class Bird(Animal):
    def __init__(self, name, age, color, wings):
        super().__init__(name, age, color)
        self.wings = wings

    def make_sound(self):
        print("фью фью")

    def eat(self):
        print("я клюю зерно")

    def to_dict(self):
        data = super().to_dict()
        data["wings"] = self.wings
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"], data["color"], data["wings"])

class Mammal(Animal):
    def __init__(self, name, age, color, legs):
        super().__init__(name, age, color)
        self.legs = legs

    def make_sound(self):
        print("мяу мяу")

    def eat(self):
        print("я ем траву")

    def to_dict(self):
        data = super().to_dict()
        data["legs"] = self.legs
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"], data["color"], data["legs"])

class Reptile(Animal):
    def __init__(self, name, age, color, tail):
        super().__init__(name, age, color)
        self.tail = tail

    def make_sound(self):
        print("шшшшшшшшшшшшш")

    def eat(self):
        print("я кушаю, кого заглотил")

    def to_dict(self):
        data = super().to_dict()
        data["tail"] = self.tail
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"], data["color"], data["tail"])

class Employee:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "age": self.age,
            "job": self.job
        }

    @classmethod
    def from_dict(cls, data):
        if data["type"] == "Zoologist":
            return Zoologist(data["name"], data["age"])
        elif data["type"] == "Veterinarian":
            return Veterinarian(data["name"], data["age"])
        else:
            raise ValueError("Неизвестный тип сотрудника")

class Zoologist(Employee):
    def __init__(self, name, age):
        super().__init__(name, age, job="Зоолог")

    def feed_animal(self, animal, zoo):
        if animal in zoo.animals:
            print(f"{self.name} кормит {animal.name}.")
        else:
            print(f"{animal.name} отсутствует в этом зоопарке.")

class Veterinarian(Employee):
    def __init__(self, name, age):
        super().__init__(name, age, job="Ветеринар")

    def heal_animal(self, animal, zoo):
        if animal in zoo.animals:
            print(f"{self.name} лечит {animal.name}.")
        else:
            print(f"{animal.name} отсутствует в этом зоопарке.")

class Zoo:
    def __init__(self):
        self.animals = []
        self.employees = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def add_employee(self, employee):
        self.employees.append(employee)

    def save_to_file(self, filename):
        data = {
            "animals": [animal.to_dict() for animal in self.animals],
            "employees": [employee.to_dict() for employee in self.employees]
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.animals = []
            self.employees = []

            for animal_data in data["animals"]:
                if animal_data["type"] == "Bird":
                    self.animals.append(Bird.from_dict(animal_data))
                elif animal_data["type"] == "Mammal":
                    self.animals.append(Mammal.from_dict(animal_data))
                elif animal_data["type"] == "Reptile":
                    self.animals.append(Reptile.from_dict(animal_data))

            for employee_data in data["employees"]:
                self.employees.append(Employee.from_dict(employee_data))
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла {filename}. Неверный формат JSON.")

    def print_zoo_info(self):
        if not self.animals and not self.employees:
            print("Зоопарк пуст.")
            return

        if self.animals:
            print("Животные в зоопарке:")
            for animal in self.animals:
                print(f" - {animal.name} ({animal.__class__.__name__}), возраст: {animal.age}, цвет: {animal.color}")
        else:
            print("В зоопарке нет животных.")

        if self.employees:
            print("\nСотрудники зоопарка:")
            for employee in self.employees:
                print(f" - {employee.name}, возраст: {employee.age}, должность: {employee.job}")
        else:
            print("\nВ зоопарке нет сотрудников.")

# Функции для демонстрации полиморфизма
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()

def animal_eat(animals):
    for animal in animals:
        animal.eat()

# Создаем зоопарк
zoo = Zoo()

# Добавляем животных
zoo.add_animal(Bird("Сыч", 1, "черный", 2))
zoo.add_animal(Mammal("Пантера", 5, "пятнистая", 4))
zoo.add_animal(Reptile("Удав", 1, "желтый", 1))

# Добавляем сотрудников
zoo.add_employee(Zoologist("Анна Юрьевна", 30))
zoo.add_employee(Veterinarian("Максим Петрович", 45))

# Сохраняем зоопарк в файл
zoo.save_to_file("zoo_data.json")

# Загружаем зоопарк из файла
new_zoo = Zoo()
new_zoo.load_from_file("zoo_data.json")

# Выводим информацию о загруженном зоопарке
new_zoo.print_zoo_info()

# Демонстрация полиморфизма
animal_sound(new_zoo.animals)
animal_eat(new_zoo.animals)
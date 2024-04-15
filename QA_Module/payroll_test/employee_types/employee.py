from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, first_name, last_name, social_security_number):
        self._first_name = first_name
        self._last_name = last_name
        self._social_security_number = social_security_number

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def social_security_number(self):
        return self._social_security_number

    @abstractmethod
    def earnings(self):
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}\n" \
               f"social security number: {self.social_security_number}"

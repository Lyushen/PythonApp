from employee_types.employee import Employee  # Assuming Employee class is defined in a separate module

import locale
locale.setlocale(locale.LC_ALL, 'en_IE.UTF-8')


class SalariedEmployee(Employee):
    def __init__(self, first, last, ssn, salary):
        super().__init__(first, last, ssn)
        self.weekly_salary = salary  # validate salary via property

    @property
    def weekly_salary(self):
        return self._weekly_salary

    @weekly_salary.setter
    def weekly_salary(self, value):
        if value < 0:
            raise ValueError("WeeklySalary must be >= 0")
        self._weekly_salary = value

    def earnings(self):
        return self.weekly_salary

    def __str__(self):
        return f"salaried employee: {super().__str__()}\nweekly salary: {locale.currency(self.weekly_salary, grouping=True)}"

import locale

from employee_types.employee import Employee  # Assuming Employee class is defined in a separate module


class HourlyEmployee(Employee):
    def __init__(self, first, last, ssn, wage, hours):
        super().__init__(first, last, ssn)
        self.hourly_wage = wage  # validate wage via property
        self.hours_worked = hours  # validate hours via property

    @property
    def hourly_wage(self):
        return self._hourly_wage

    @hourly_wage.setter
    def hourly_wage(self, value):
        if value < 0:
            raise ValueError("Hourly wage must be >= 0")
        self._hourly_wage = value

    @property
    def hours_worked(self):
        return self._hours_worked

    @hours_worked.setter
    def hours_worked(self, value):
        if value < 0 or value > 168:  # Assuming maximum hours in a week is 168
            raise ValueError("Hours worked must be between 0 and 168")
        self._hours_worked = value

    def earnings(self):
        if self.hours_worked <= 40:
            return self.hourly_wage * self.hours_worked
        else:
            return 40 * self.hourly_wage + (self.hours_worked - 40) * self.hourly_wage * 1.5

    def __str__(self):
        return f"hourly employee: {super().__str__()}\nhourly wage: {locale.currency(self.hourly_wage)}\nhours worked: {self.hours_worked}"

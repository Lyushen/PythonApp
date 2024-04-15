import locale

from employee_types.employee import Employee  # Assuming Employee class is defined in a separate module


class CommissionEmployee(Employee):
    def __init__(self, first, last, ssn, sales, rate):
        super().__init__(first, last, ssn)
        self.gross_sales = sales
        self.commission_rate = rate

    @property
    def gross_sales(self):
        return self._gross_sales

    @gross_sales.setter
    def gross_sales(self, value):
        if value < 0:
            raise ValueError("Gross sales must be >= 0")
        self._gross_sales = value

    @property
    def commission_rate(self):
        return self._commission_rate

    @commission_rate.setter
    def commission_rate(self, value):
        if not 0 <= value <= 1:
            raise ValueError("Commission rate must be between 0 and 1")
        self._commission_rate = value

    def earnings(self):
        return self.gross_sales * self.commission_rate

    def __str__(self):
        return f"Commission Employee: {super().__str__()}\nGross Sales: {locale.currency(self.gross_sales, grouping =True)}\nCommission Rate: {self.commission_rate:.2%}"


class BasePlusCommissionEmployee(CommissionEmployee):
    def __init__(self, first, last, ssn, sales, rate, salary):
        super().__init__(first, last, ssn, sales, rate)
        self.base_salary = salary

    @property
    def base_salary(self):
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value):
        if value < 0:
            raise ValueError("Base Salary must be >= 0")
        self._base_salary = value

    def earnings(self):
        return super().earnings() + self.base_salary

    def __str__(self):
        return f"Base Plus Commission Employee: {super().__str__()}\nBase Salary: {locale.currency(self.base_salary)}"


from employee_types.commissionemployees import CommissionEmployee, BasePlusCommissionEmployee
from employee_types.hourlyemployees import HourlyEmployee
from employee_types.pieceworker import PieceWorker
from employee_types.salariedemployee import SalariedEmployee
import locale
import pickle

def main():
    employees = []

    print("\nCreate Salaried Employee\n")
    first_name = input("Enter Salaried Employee FirstName: ")
    last_name = input("Enter Salaried Employee LastName: ")
    ssn = input("Enter Salaried Employee SSN: ")
    salary = float(input("Enter Salaried Employee Salary: "))
    employees.append(SalariedEmployee(first_name, last_name, ssn, salary))

    print("\nCreate Hourly Employee\n")
    first_name = input("Enter Hourly Employee FirstName: ")
    last_name = input("Enter Hourly Employee LastName: ")
    ssn = input("Enter Hourly Employee SSN: ")
    rate = float(input("Enter Hourly Employee Rate Per Hour (> 0): "))
    hours = float(input("Enter Hourly Employee Hours Worked (0 to 168): "))
    employees.append(HourlyEmployee(first_name, last_name, ssn, rate, hours))

    print("\nCreate Commission Employee\n")
    first_name = input("Enter Commission Employee FirstName: ")
    last_name = input("Enter Commission Employee LastName: ")
    ssn = input("Enter Commission Employee SSN: ")
    sales = float(input("Enter Commission Employee Sales (> 0): "))
    comm_rate = float(input("Enter Commission Employee Commission rate (> 0 and < 1): "))
    employees.append(CommissionEmployee(first_name, last_name, ssn, sales, comm_rate))

    print("\nCreate Base Plus Commission Employee\n")
    first_name = input("Enter Base Plus Commission Employee FirstName: ")
    last_name = input("Enter Base Plus Commission Employee LastName: ")
    ssn = input("Enter Base Plus Commission Employee SSN: ")
    sales = float(input("Enter Base Plus Commission Employee Sales (> 0): "))
    comm_rate = float(input("Enter Base Plus Commission Employee Commission rate (> 0 and < 1): "))
    base_salary = float(input("Enter Base Plus Commission Employee Base Salary (> 0): "))
    employees.append(BasePlusCommissionEmployee(first_name, last_name, ssn, sales, comm_rate, base_salary))

    print("\nCreate Piece Worker Employee\n")
    first_name = input("Enter Piece Worker Employee FirstName: ")
    last_name = input("Enter Piece Worker Employee LastName: ")
    ssn = input("Enter Piece Worker Employee SSN: ")
    items_produced = float(input("Enter Piece Worker Employee Items Produced (> 0): "))
    rate_per_item = float(input("Enter Piece Worker Employee Rate Per Item (> 0): "))
    employees.append(PieceWorker(first_name, last_name, ssn, items_produced, rate_per_item))

    print("\nEmployees processed polymorphically:\n")

    for current_employee in employees:
        print(current_employee)  # invokes __str__
        print(f"Earned {locale.currency(current_employee.earnings())}\n")



if __name__ == "__main__":
    main()
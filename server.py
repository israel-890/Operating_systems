import os
import sys
from customer import Customer
from dateutil.parser import parse
import re

class Validation():

    def is_valid_id(id_number):
        if len(id_number) > 9:
            return False
        try:
            id_number = int(id_number)
        except ValueError:
            return False
        sum_digits = 0
        for i, digit in enumerate(str(id_number)[:-1]):
            multiplier = 1 if i % 2 == 0 else 2
            sum_digits += multiplier * int(digit)
        check_digit = 10 - (sum_digits % 10)
        if check_digit != int(str(id_number)[-1]):
            return False
        return True
     
    def is_valid_phone(phone_num):
        if phone_num[0] != "0":
            return False
        if len(phone_num) > 10 or len(phone_num) < 9:
            return False
        try:
            int(phone_num)
        except ValueError:
            return False
        else:
            return True
    
    def is_valid_date(date):
        try:
            parse(date)
            return True
        except ValueError:
            return False
       
    def is_money_amount(sum):
        money_pattern = re.compile(r'^\d+(\.\d{1,2})?$')
        if money_pattern.match(sum):
            return True
        else:
            return False   
    
class Customer:
    def __init__(self, first, last, id, phone, debt, date):
        self._first = first
        self._last = last
        self._id = id
        self._phone = phone
        self._debt = debt
        self._date = date

    @property
    def id(self):
        return self._id
    
    def __str__(self):
        return f"name: {self._first}{self._last} ID:{self._id} phone:{self._phone}"
    
    def add_debt(self, new_debt):
        self._debt += new_debt

class Customers_list():
    def __init__(self):
        self.customers = []
    
    def add_custemer(self, new_custemer):        
        id = new_custemer[2]
        for customer in self.customers:
            if customer.id == id:
                customer.add_debt(float(new_custemer[4]))
                break
        else:
            customer = Customer(*new_custemer)
            self.customers.append(customer)
    def __str__(self):
        customer_info = [str(customer) for customer in self.customers]
        return "\n".join(customer_info)
    
    def sort_by_debt(self):
        print("in sort")
        self.customers.sort(key=lambda x: x._debt)
        print(customers_list)

    def sort_by_debt_mini(self):
        print("in sort")
        self.customers.sort(key=lambda x: x._debt, reverse=True)
        print(customers_list)


if len(sys.argv) < 2:
    print("Eror: missing csv file name!")
    quit()

csv_file = sys.argv[1]
if not os.path.exists(csv_file):
    with open(csv_file, "w"):
        pass

customers_list = Customers_list()
with open(csv_file, "r") as fd:
    for line in fd.readlines():
        file_line_dtb = line.split(",")
        customers_list.add_custemer(file_line_dtb)


    
while True:
    query = input("==> ")
    if query == "quit":
        print("exit!")
        break
    if query == 'print':
        print(customers_list)
    if query == "sort":
        customers_list.sort_by_debt()
    if query == "sort_mini":
        customers_list.sort_by_debt_mini()
        
    
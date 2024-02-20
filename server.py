import os
import sys
# from customer import Customer
from datetime import datetime, date
import re

class Validation():

    def valid_id(id_number):
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
    
    def check_name(name1, last1, first, last):
        if name1 == first or name1 == None:
            name1 = first
        else:
            print(f"The name {first} does not match the name on this ID!")
            choss = input(f"Do you to switch the name {first} to {name1}? y/n")
            if choss == "y":
                first = name1
            else:
                return
        if last1 == last or last1 == None:
            last1 = last
        else:
            print(f"The name {last} does not match the name on this ID!")
            choss = input(f"Do you to switch the name {last} to {last1}? y/n")
            if choss == "y":
                last = last1
            else:
                return
        print("the names is correct!")
     
    def valid_phone(phone_num):
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
    
    def valid_date(date):
        try:
            datetime.strptime(date, "%d.%m.%y")
            datetime.strptime(date, "%d/%m/%y")
            return True
        except ValueError:
            return False
       
    def money_amount(sum):
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
    def first(self):
        return self._first
    
    @property
    def last(self):
        return self._last
    
    @property
    def id(self):
        return self._id
    
    @property
    def phone(self):
        return self._phone
    
    @property
    def debt(self):
        return self._debt
    
    @property
    def date(self):
        return self._date
    

    def __str__(self):
        return f"name: {self.first}{self.last} ID:{self.id} phone:{self.phone} debt:{self.debt} date:{self.date}"
    
    def add_debt(self, new_debt):
        self.debt += new_debt

    def update_date(self, date1, date2):
        if date1 > date2:
            return date1
        else:
            return date2    

class Customers_list():
    def __init__(self):
        self.customers:list[Customer] = []
    
    def add_custemer(self, new_customer:list[str]):
        id = new_customer[2]
        for customer in self.customers:
            if customer.id == id:
                customer.check_name(new_customer[0], new_customer[1], customer.first, customer.last) #שים לב לייצר פונקציית בדיקת שמות
                customer.add_debt(float(new_customer[4]))
                customer.date = customer.update_date(new_customer[5], customer.date)
                break
        else:
            customer = Customer(*new_customer)
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
        self.customers.sort(key=lambda x: x.debt, reverse=True)
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


validation = Validation()
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
    if query == "add_client":
        names = ["first_name", "last_name", "id", "phone_number", "debt", "date"]
        values = [input(f"Enter a {name}: ") or 'Empty No input entered!' for name in names]
        if not validation.valid_id(values[2]): 
            print("Error: the id didn't put or not correct!")
        if not validation.valid_phone(values[3]):
            print("Error: the phone didn't put or not correct!")
        if not validation.money_amount(values[4]):
            print("Error: the debt didn't put or not correct!")
        if not validation.valid_date(values[5]):
            print("Error: the date didn't put or not correct!")
        print(f" thas is the added {values}")
        customers_list.add_custemer(values)
            
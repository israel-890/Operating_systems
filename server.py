import os
import sys
from validation import Validation
# import socket
# from threading import Thread


class Customer:
    def __init__(self, first, last, id, phone, debt, date):
        self._first = first
        self._last = last
        self._id = id
        self._phone = phone
        self.debt = debt
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
    def date(self):
        return self._date
    
    @date.setter
    def date(self, new_date):
        self._date = new_date
    
    def __str__(self):
        return f"name: {self.first}{self.last} ID:{self.id} phone:{self.phone} debt:{self.debt} date:{self.date}"
    
    def add_debt(self, new_debt):
        current_debt = float(self.debt)

        new_debt = float(new_debt)
        total_debt = current_debt + new_debt

        self.debt = str(total_debt)

    def update_date(self, date1, date2):
        if date1 > date2:
            return date1
        else:
            return date2    


class CustomersList():
    def __init__(self):
        self.customers:list[Customer] = []
    
    def create_customers_list(self, file_name):
        if not os.path.exists(file_name):
            with open(file_name, "w"):
                pass
        line_number = 0
        with open(file_name, "r") as fd:
            for line in fd.readlines():
                line_number += 1
                if len(line.split(",")) != 6:
                    print(f"line error: {line_number} Incorrect number of entries")
                else:
                    file_line_dtb = line.lower().strip().split(",")
                    if not validation.valid_id(file_line_dtb[2]): 
                        print("Error: ID does not exist or not correct!")
                    if not validation.valid_phone(file_line_dtb[3]):
                        print("Error: Phone number does not exist or not correct!")
                    if not validation.money_amount(file_line_dtb[4]):
                        print("Error: the debt does not exist or not correct!")
                    if not validation.valid_date(file_line_dtb[5]):
                        print("Error: the date does not exist or not correct or year without 4 digits !")
                    self.add_customer(file_line_dtb)

    def add_customer(self, new_customer:list[str]):
        id = new_customer[2]
        for customer in self.customers:
            if customer.id == id:
                validation.check_name(new_customer[0], new_customer[1], customer.first, customer.last)
                customer.add_debt(float(new_customer[4]))
                customer.date = customer.update_date(new_customer[5], customer.date)
                break
        else:
            customer = Customer(*new_customer)
            self.customers.append(customer)
    
    def delete_customer(self, id):
        for i in self.customers:
            if i.id == str(id):
                self.customers.remove(i)  
                print( f"Customer with ID {id} deleted successfully!")
                return
        print (f"Customer with ID {id} not found!")

    def __str__(self):
        customer_info = [str(customer) for customer in self.customers]
        return "\n".join(customer_info)
    
    def sort_by_debt(self):
        print("sorting...")
        self.customers.sort(key=lambda x: x.debt)
        print(self.__str__())

    def sort_and_print(self):
        self.customers.sort(key=lambda x: x.debt, reverse=True)
        print(self.__str__())


def handle_request(query, customers_instance, valid_instance):
    if query == "quit":
        quit()
    elif query == "print":
        customers_instance.sort_and_print()
    elif query == "sort":
        customers_instance.sort_by_debt()
    elif query == "remove_client":
        remove = input("How to remove? enter ID: ")
        customers_instance.delete_customer(remove)
    elif query == "add_client":
        names = ["first_name","last_name","id","phone_number","debt","date"]
        values = []
        for name in names:
            try:
                value = input(f"Enter a {name}: ")
            except ValueError:
                value = 'Empty No input entered!'
            values.append(value)
        if not valid_instance.valid_id(values[2]):
            print("Error: ID does not exist or not correct!")
            return None
        if not valid_instance.valid_phone(values[3]):
            print("Error: phone does not exist or not correct!")
            return None
        if not valid_instance.money_amount(values[4]):
            print("Error: the debt does not exist or not correct!")
            return None
        if not valid_instance.valid_date(values[5]):
            print("Error: the date does not exist or not correct or year without 4 digits!")
            return None
        print(f"thees is the added {values}")
        customers_instance.add_customer(values)
    else:
        print(f"Unknown request: {query}")
        return None


customers_list = CustomersList()
validation = Validation()
def main():
    if len(sys.argv) < 2:
        print("Error: missing csv file name!")
        quit()
    customers_list.create_customers_list(sys.argv[1])
    exit = False
    while not exit:
        query = input("Enter your query:(print/sort/add_client/remove_client/quit) ")
        handle_request(query, customers_list, validation)
        
if __name__ == '__main__':
    main()
               
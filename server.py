import os
import sys
# from customer import Customer
from validation import Validation
from datetime import datetime, date
import socket
import time
from threading import Thread


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
    
    @debt.setter
    def debt(self, new_debt):
        self._debt = new_debt
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, new_date):
        self._date = new_date
    

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
    
    def create_customers_list(self):
        csv_file = sys.argv[1]
        if not os.path.exists(csv_file):
            with open(csv_file, "w"):
                pass
        line_number = 0
        with open(csv_file, "r") as fd:
            for line in fd.readlines():
                line_number += 1
                file_line_dtb = line.split(",")
                if len(file_line_dtb) == 6:
                    if not validation.valid_id(file_line_dtb[2]): 
                        print("Error: the id didn't put or not correct!")
                    if not validation.valid_phone(file_line_dtb[3]):
                        print("Error: the phone didn't put or not correct!")
                    if not validation.money_amount(file_line_dtb[4]):
                        print("Error: the debt didn't put or not correct!")
                    if not validation.valid_date(file_line_dtb[5]):
                        print("Error: the date didn't put or not correct!")
                elif len(file_line_dtb) < 6:
                    print(f"Line {line_number} is missing data!")
                customers_list.add_customer(file_line_dtb)

    def add_customer(self, new_customer:list[str]):
        id = new_customer[2]
        for customer in self.customers:
            if customer.id == id:
                Validation.check_name(new_customer[0], new_customer[1], customer.first, customer.last)
                customer.add_debt(float(new_customer[4]))
                customer.date = customer.update_date(new_customer[5], customer.date)
                break
        else:
            customer = Customer(*new_customer)
            self.customers.append(customer)
    
    def delete_customer(self, id):
        customer = customers_list.
        
        find(lambda c: c.id == id)


        if customer:
            customers_list.remove(customer)
            return f"Customer with ID {id} deleted successfully!"

        # אם הלקוח לא נמצא
        return f"Customer with ID {id} not found!"

    
    def __str__(self):
        customer_info = [str(customer) for customer in self.customers]
        return "\n".join(customer_info)
    
    def sort_by_debt(self):
        print("sorting...")
        self.customers.sort(key=lambda x: x._debt)
        print(customers_list)

    def sort_and_print(self):
        self.customers.sort(key=lambda x: x.debt, reverse=True)
        print(customers_list)


def handle_connection(client_socket, server_socket):
    data = client_socket.recv(1024)
    
    print(f"Received data: {data.decode('utf-8')}")
    query = data.decode('utf-8')

    t = Thread(target=_handle_request, args=(query, client_socket))
    t.start()
    if query == "bay" or query == "quit":
        exit = True
        return exit
    return query


def _handle_request(query, client_socket):
    if query == "print":
        customers_list.sort_and_print()
    elif query == "sort":
        customers_list.sort_by_debt()
    elif query == "add_client":
        names = ["first_name", "last_name", "id", "phone_number", "debt", "date"]
        values = [input(f"Enter a {name}: ") or 'Empty No input entered!' for name in names]
        if not validation.valid_id(values[2]):
            print("Error: the id didn't put or not correct!")
            return None
        if not validation.valid_phone(values[3]):
            print("Error: the phone didn't put or not correct!")
            return None
        if not validation.money_amount(values[4]):
            print("Error: the debt didn't put or not correct!")
            return None
        if not validation.valid_date(values[5]):
            print("Error: the date didn't put or not correct!")
            return None
        print(f"thees is the added {values}")
        customers_list.add_customer(values)
    else:
        print(f"Unknown request: {query}")
        return None
    
exit = False
customers_list = Customers_list()
customers_list.create_customers_list()
validation = Validation()

host = '127.0.0.1'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

def main():
    if len(sys.argv) < 2:
        print("Error: missing csv file name!")
        quit()

    while not exit:
        try:
            client_socket, client_address = server_socket.accept()
        except OSError:
            break
        print(f"Accepted connection from {client_address}")
        t = Thread(target=handle_connection, args=(client_socket, server_socket))
        t.start()
        

if __name__ == '__main__':
    main()
               
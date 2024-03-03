import os
import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


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
        return f"name: {self.first} {self.last} ID:{self.id} phone:{self.phone} debt:{self.debt} date:{self.date}"
    
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
    
    def create_customers_list(self, file_name, socket):
        if not os.path.exists(file_name):
            with open(file_name, "w"):
                pass
        line_number = 0
        with open(file_name, "r") as fd:
            for line in fd.readlines():
                line_number += 1
                if len(line.split(",")) != 6:
                    send_response(socket, f"line error: {line_number} Incorrect number of entries")
                else:
                    file_line_dtb = line.lower().strip().split(",")
                    if not validation.valid_id(file_line_dtb[2]): 
                        send_response(socket, "Error: ID does not exist or not correct!")
                    if not validation.valid_phone(file_line_dtb[3]):
                        send_response(socket, "Error: Phone number does not exist or not correct!")
                    if not validation.money_amount(file_line_dtb[4]):
                        send_response(socket, "Error: the debt does not exist or not correct!")
                    if not validation.valid_date(file_line_dtb[5]):
                        send_response(socket, "Error: the date does not exist or not correct or year without 4 digits !")
                    self.add_customer(file_line_dtb)

    def add_customer(self, new_customer:list[str]):
        id = new_customer[2]
        for customer in self.customers:
            if customer.id == id:
                validation.check_name(new_customer[0].lower(), new_customer[1].lower(), customer.first, customer.last)
                customer.add_debt(float(new_customer[4]))
                customer.date = customer.update_date(new_customer[5], customer.date)
                break
        else:
            customer = Customer(*new_customer)
            self.customers.append(customer)
    
    def delete_customer(self, id, sock):
        for i in self.customers:
            if i.id == str(id):
                self.customers.remove(i)  
                send_response(sock, f"Customer with ID {id} deleted successfully!")
                return
        send_response(sock,f"Customer with ID {id} not found!")

    def __str__(self):
        customer_info = [str(customer) for customer in self.customers]
        return "\n".join(customer_info)
    
    def sort_by_debt(self, sock):
        send_response(sock,"sorting...")
        self.customers.sort(key=lambda x: x.debt)
        send_response(sock, self.__str__())

    def sort_and_print(self, sock):
        self.customers.sort(key=lambda x: x.debt, reverse=True)
        send_response(sock,self.__str__())


class Validation():

    @staticmethod
    def valid_id(id_number):
        if len(str(id_number)) > 9:
            return False
        try:
            id_number = int(id_number)
        except ValueError:
            return False
        sum_digits = 0
        for digit in str(id_number)[1::2]:
            multiplier = int(digit) * 2
            if multiplier > 9:
                multiplier = int(str(multiplier)[0]) + int(str(multiplier)[1])
            sum_digits += multiplier 
        for digit in str(id_number)[0::2]:
            sum_digits += int(digit)
        if sum_digits % 10 != 0:
            return False
        return True

    @staticmethod
    def check_name(name1, last1, first, last):
        if name1 == first or name1 == None:
            name1 = first
        else:
            send_response(socket, f"The name '{first}' does not match the name on this ID!")
            send_response(socket, f"Do you to switch the name '{first}' with '{name1}'? y/n")
            chose = receive_request(socket)
            if chose == "y":
                first = name1
            else:
                return
        if last1 == last or last1 == None:
            last1 = last
        else:
            send_response(socket, f"The name '{last}' do not match the name on this ID!"
            "Do you to switch the name '{last}' with '{last1}'? y/n")
            chose = receive_request(socket)
            if chose == "y":
                last = last1
            else:
                return
        send_response(socket, "the names is correct!")
     
    @staticmethod
    def valid_phone(phone_num):
        if phone_num[0] == ('0'):
            return phone_num[1:].isdigit() and len(phone_num) == 10
        else:
            return False

    @staticmethod
    def valid_date(my_date):
        try:
            return datetime.strptime(my_date, "%d/%m/%Y").date()
        except ValueError:
            send_response(socket, "Invalid input of date format.")
            return False
        
    @staticmethod
    def money_amount(sum):
        try:
            float(sum)
            return True
        except:
            send_response(socket,"Error: the debt is not correct!")


def receive_request(sock):
    data = sock.recv(1024).decode("utf-8").strip()
    return data

def send_response(sock, response):
    sock.sendall(response.encode("utf-8"))

def handle_request(query, customers_instance, validation, sock):
    if query == "quit":
        send_response(sock, "Goodbye!")
        return
    elif query == "print":
        customers_instance.sort_and_print(sock)
    elif query == "sort":
        customers_instance.sort_by_debt(sock)
    elif query == "remove_client":
        send_response(sock, "How to remove? Enter ID: ")
        remove_id = receive_request(sock)
        customers_instance.delete_customer(remove_id, sock)
    elif query == "add_client":
        names = ["first_name", "last_name", "id", "phone_number", "debt", "date"]
        values = []
        for name in names:
            try:
                send_response(sock, f"Enter a {name}: ")
                value = receive_request(sock)
            except ValueError:
                value = 'Empty No input entered!'
            values.append(value)
        if not validation.valid_id(values[2]):
            send_response(sock, "Error: ID does not exist or not correct!")
            return None
        if not validation.valid_phone(values[3]):
            send_response(sock, "Error: phone does not exist or not correct!")
            return None
        if not validation.money_amount(values[4]):
            send_response(sock, "Error: the debt does not exist or not correct!")
            return None
        if not validation.valid_date(values[5]):
            send_response(sock, "Error: the date does not exist or not correct or year without 4 digits!")
            return None
        send_response(sock, f"Added {values} successfully added!!")
        customers_instance.add_customer(values)
    else:
        send_response(sock, f"Unknown request: {query}")

customers_list = CustomersList()  
validation = Validation()  

def main():
    if len(sys.argv) < 2:
        print("Error: missing csv file name!")
        quit()

    server_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 8080))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        thread = Thread(target=handle_request, args=(receive_request(client_socket), customers_list, validation, client_socket))
        thread.start()

    server_socket.close()

if __name__ == '__main__':
    main()
               
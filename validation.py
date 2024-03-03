from datetime import datetime
from socket import socket
from server import receive_request, send_response 

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
            
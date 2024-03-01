from datetime import datetime


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
            print(f"The name {first} does not match the name on this ID!")
            chose = input(f"Do you to switch the name {first} to {name1}? y/n")
            if chose == "y":
                first = name1
            else:
                return
        if last1 == last or last1 == None:
            last1 = last
        else:
            print(f"The name {last} does not match the name on this ID!")
            chose = input(f"Do you to switch the name {last} to {last1}? y/n")
            if chose == "y":
                last = last1
            else:
                return
        print("the names is correct!")
     
    @staticmethod
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
    
    @staticmethod
    def valid_date(date):
        try:
            datetime.strptime(date, "%d.%m.%y")
            datetime.strptime(date, "%d/%m/%y")
            return True
        except ValueError:
            return False
        
    @staticmethod
    def money_amount(sum):
        try:
            float(sum)
            return True
        except:
            print("Error: the debt is not correct!")
            
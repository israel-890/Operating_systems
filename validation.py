from datetime import datetime, date


class Validation():

    @staticmethod
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
import os
import sys
from customer import Customer


def is_valid_id(id_number):
    if len(id_number) != 9:
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


if len(sys.argv) < 2:
    print("Eror: missing csv file name!")
    quit()

csv_file = sys.argv[1]
if not os.path.exists(csv_file):
    with open(csv_file, "w"):
        pass

customers = []
with open(csv_file, "r") as fd:
    for line in fd.readlines():
        file_line_dtb = line.split(",")
        exists = False
        id = int(file_line_dtb[2])
        for i, customer in enumerate(customers):
            if customer.id == id:
                exists = i
                break
        if exists >= 0:
            customer[exists].add_debt(int(file_line_dtb[4]))
        else:
            customer = customer(*file_line_dtb)
            customers.append(customer)
customers.sort(key=lambda customer:customer.debt)
for customer in customers:
    print(customer)
    


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

    
    
    
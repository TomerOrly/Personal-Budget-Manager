class Transaction:
    def __init__(self, id, date,type,category, description,amount):
        self.id = id
        self.date = date
        self.type = type
        self.category = category
        self.description = description
        self.amount = amount

    def __str__(self):
        return f"ID: {self.id}, Date: {self.date}, Type: {self.type}, Category: {self.category}, Description: {self.description}, Amount: {self.amount}"

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "category": self.category,
            "description": self.description,
            "amount": self.amount
        }

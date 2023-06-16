
class Category:
    import math
    def __init__ (self, cate):
        self.name = cate
        self.ledger = []
        self.balance = 0.0

    def __repr__(self):
        header = f"{self.name:*^30}\n"
        ledger = ""
        for item in self.ledger:
            line_description = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        total = "Total: {:.2f}".format(self.balance)
        return header + ledger + total

    def deposit(self, amount, *args):
        self.balance += amount
        description = args[0] if args else ""
        self.ledger.append({"amount": amount, "description": description})
        

    def withdraw(self, amount, *args):
        description = args[0] if args else ""
        if (self.check_funds(amount)):
            self.balance -= amount
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return self.balance
        
    def transfer(self, amount, category_instance):
        if self.withdraw(amount, "Transfer to {}".format(category_instance.name)):
            category_instance.deposit(amount, "Transfer from {}".format(self.name))
            return True
        else:
            return False
    
    def check_funds(self, amount):
        if self.balance >= amount:
            return True
        return False
    
def create_spend_chart(categories):
    spent_amounts = []
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    header = "Percentage spent by category\n"
    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"
    return (header + chart + footer).rstrip("\n")




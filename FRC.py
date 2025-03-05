import pandas
from tabulate import tabulate
from datetime import date
# this one makes a decorated statements
def make_statement(statement, decoration, lines=1):
    """This one makes a decorated statement, defaults to a single line
    :parameter statement, decoration, lines(optional)
    :return nothing!
    """
    res=""
    lines = int(lines)
    for i in range(0, lines):
        if i == int(lines / 2):
            res=res+f"{decoration * 3} {statement} {decoration * 3}\n"
        else:
            res+=decoration * (len(statement) + 8) +"\n"
    return res
def instruction():
    make_statement("Instruction","ℹ️")
    print("""
    
For each ticket holder enter ...
- Their name
- Their age
- The payment method (cash / credit)

THe program will record the ticket sale and calculate the ticket cost (and the profit).

Once you have either sold all of the tickets or entered the exit code ('xxx'), the program will display the ticket
sales information and write the data to a text file.

It will also choose one lucky ticket holder who wins the draw (their ticket is free).

    """)

def not_blank(question):
    """ check if the input is blank to make sure the return of this function is not blank"""
    print(question,end="")
    while True:
        response = input()
        if response == "":
            print("Sorry, this can't be blank...")
            continue
        return response


def yes_no(question):
    while True:
        response = input(question).lower()
        if response == "yes" or response == "y":
            return True
        if response == "no" or response == "n":
            return False
        print("""Please enter either "yes"(y) or "no"(n) """)


def string_checker(question, valid_ans_list=("yes", "no"), num_letters=1):
    """ This function check what user wants from the list showed by checking if they input the specific amount of letter(s) or full letter(s) of a valid option on the list"""
    while True:
        response = input(question).lower()
        for item in valid_ans_list:
            if response == item or response == item[:num_letters]:  # i[:j] means taking the element from first index 0 to before index j.
                return item
        print(f"Please choose a valid answer from {valid_ans_list}")


def num_check(question, num_type, exitcode):
    """ This function checking and make sure that it returns a valid integer or float"""
    print(question,end="")
    if num_type == "integer" or num_type == "int":
        num_type = int
        value_error_announcement = "please enter an integer (ie: a number which does not have a decimal part)."
        lesser_announcement = "please enter an integer that is more than 0"
    else:
        num_type = float
        value_error_announcement = "please enter a number"
        lesser_announcement = "please enter a number that is more than 0"

    while True:
        try:
            response = input()
            if response=="":
                return ""
            response=num_type(response)
            if response <= 0:
                print(lesser_announcement)
                continue
            if exitcode:
                return response
            return
        except ValueError:
            print(value_error_announcement)


# def int_check(question,name):
#     """ This function check if their age are available to buy a ticket and output their name with the result, ie: "A is too young"""
#     print(question,end="")
#     while True:
#         try:
#             response = int(input())
#             if response < 12:
#                 print(f"Sorry you are too young for this movie")
#                 return False
#             elif response > 120:
#                 print(f"?? That looks like a typo (too old)")
#                 return False
#             elif response >=12 and response<16:
#                 # First return element is for the if condition in main to see if the program should continue because users age is in valid boundary
#                 # Second element return the index/position of their ticket type in the list in main: 0 for children, 1 for adult, 2 for senior
#                 return True , 0
#             elif response >=16 and response<65:
#                 return True, 1
#             elif response >=65 and response<121:
#                 return True, 2
#         except ValueError:
#             print("<Please enter an integer>")

def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)

def get_expenses(exp_type,default_item_quanity=1):
    """:return the frame for pandas""" 
    all_item_name=[]
    all_item_quanity=[]
    all_item_cost=[]

    # expenses dict
    data_dict={
        "Item":all_item_name,
        "Amount":all_item_quanity,
        "$ / Item":all_item_cost
    }
    if exp_type=="fixed":
        how_much_question="How much? $"
    else:
        how_much_question="Price for one: $"
    while True:
        response=not_blank("Item name: ")
        if response!="xxx":
            # name of item
            all_item_name.append(response)
            item_quanity=num_check("How many: ", "int", True)
            # numer of item
            if item_quanity=="":
                item_quanity=default_item_quanity
            all_item_quanity.append(item_quanity)
            # cost of item
            item_cost=num_check(how_much_question,"float",True)
            all_item_cost.append(item_cost)
            continue
        if len(all_item_name)== 0 and exp_type=="variable":
            print(f"Oops - you have not entered anything.\nYou need at least one item.")
            continue
        break

    # make pandas
    expense_frame = pandas.DataFrame(data_dict)
    # Calculate Cost column
    expense_frame["Cost"]= expense_frame['Amount'] * expense_frame['$ / Item']
    # calculate subtotal
    subtotal = expense_frame['Cost'].sum()

    # apply currency formatting to currency columns
    add_dollars=["$ / Item", "Cost"]
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)
    if exp_type == "variable":
        expense_string=tabulate(expense_frame,headers='keys',tablefmt='psql',showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item' , 'Cost']], headers='keys', tablefmt='psql', showindex=False)
    return expense_string, subtotal


#main is here
fixed_subtotal = 0
fixed_panda_string = ""
product_name = not_blank("Product name: ")
quanity_made = num_check("Quantity being made: ", "interger", True)
variable_expense=get_expenses("variable",quanity_made)

print()

print("Getting Variable Costs...")
variable_pandas=variable_expense[0]
variable_subtotal=variable_expense[1]


# ask if user has fixed expenses and retrive them
print()

if yes_no("Do you have fixed expenses? "):
    fixed_expense=get_expenses("fixed")
    fixed_panda_string= fixed_expense[0]
    fixed_subtotal = fixed_expense[1]
print()
if fixed_subtotal == 0 :
    has_fixed = False 
    fixed_panda_string=""


print()

total_expenses = variable_subtotal + fixed_subtotal
# Get profit Goal here.

# strings / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as indiviual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# strings for printing to file
file_heading = make_statement("Fund Raising Calculator" +" "+f"{product_name}, {day}/{month}/{year}","=")
file_quanity = f"Quanity being made: {quanity_made}"
file_variable_expenses_heading = make_statement("Variable Expenses","-")
file_variable_expenses_frame = variable_pandas
file_variable_expenses_subtotal = f"Variable Expenses Subtotal: ${variable_subtotal}"
if has_fixed == False:
    file_fixed_expenses_heading = make_statement("You have no fixed expenses","-")
    file_fixed_expenses_pandas = ""
    file_fixed_expenses_subtotal = f"Fixed Expenses Subtotal: ${fixed_subtotal}"
else:
    file_fixed_expenses_heading = make_statement("Fixed Expenses","-")
    file_fixed_expenses_pandas = fixed_panda_string
    file_fixed_expenses_subtotal = f"Fixed Expenses Subtotal: ${fixed_subtotal}"
file_total_Expenses = f"Total Expenses: ${total_expenses}"

list=(
    file_heading,"\n",
    file_quanity,"\n",
    file_variable_expenses_heading,
    file_variable_expenses_frame,
    file_variable_expenses_subtotal,"\n",
    file_fixed_expenses_heading,
    file_fixed_expenses_pandas,
    file_fixed_expenses_subtotal,"\n",
    file_total_Expenses,"\n"
)
for item in list:
    print(item)

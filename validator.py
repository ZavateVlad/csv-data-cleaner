# # Exercise 1
# products = [
#     {"name": "apple", "price": 1.20},
#     {"name": "banana", "price": 0.50},
#     {"name": "orange", "price": 0.80},
#     {"name": "grape", "price": 2.50}
# ]
#
# def new_dictionary(lst):
#     empty_dict = {}
#     for element in lst:
#         key = element["name"]
#         value = element["price"]
#         #empty_dict[key] = value
#
#         if value > 1.00:
#             empty_dict[key] = value
#
#
#     return empty_dict
#
# print(new_dictionary(products))


# Exercise 2
def count_chars(text):
    freq_dict = {}

    for s in text:
        if s != " ":
            if s not in freq_dict:
                freq_dict[s] = 0
            freq_dict[s] += 1

    return freq_dict
# How to remove the space?
print(count_chars("hello world"))


# Exercise 3
ages = [12, 25, 17, 33, 19, 41, 16, 28]

result = [age + 10 for age in ages if age >= 18]
# Why is this not working?
print(result)



def read_csv(filename):
    curated_list = []
    with open(filename, 'r') as f:
        headers = f.readline().strip().split(",")
        for line in f:
            line = line.strip().split(",")
            curated_dictionary = dict(zip(headers, line))
            curated_list.append(curated_dictionary)

    return curated_list


import re


def is_valid_email(email):
    if re.match(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', email):
        return True
    else:
        return False
    # or return '@' in email and '.' in email.split('@')[1]

def is_valid_age(age_str):
    try:
        if 0 < int(age_str) < 120:
            return True
    except ValueError:
            return False
    # or try:
    #         return 0 < int(age_str) < 120
    #     except ValueError:
    #         return False

def is_not_empty(value):
    if value != "":
        return True
    else:
        return False
    # or return bool(value.strip())


def validate_customers(customers):
    """
    Validate all customer records and count errors

    Returns: dictionary with error counts
    Example: {
        'invalid_email': 3,
        'invalid_age': 2,
        'missing_name': 1,
        'missing_city': 1
    }
    """
    errors = {
        'invalid_email': 0,
        'invalid_age': 0,
        'missing_name': 0,
        'missing_city': 0
    }

    for customer in customers:
        if not is_valid_email(customer["email"]):
            errors['invalid_email'] += 1
        if not is_valid_age(customer["age"]):
            errors['invalid_age'] += 1
        if not is_not_empty(customer["name"]):
            errors['missing_name'] += 1
        if not is_not_empty(customer["city"]):
            errors['missing_city'] += 1

    return errors




def print_report(errors, total_rows):
    """Print a nice summary of validation results"""
    print("=== Validation Report ===")
    print(f"Total rows processed: {total_rows}")
    print(f"\nErrors found:")
    print(f'- Invalid email: {errors["invalid_email"]}')
    print(f'- Invalid age: {errors["invalid_age"]}')
    print(f'- Invalid name: {errors["missing_name"]}')
    print(f'- Invalid city: {errors["missing_city"]}')
    sum_errors = sum(errors.values())
    print(f'Total errors: {sum_errors}')
    percentage = 100 - ((sum_errors * 100) / total_rows)
    print(f'Success rate: {percentage}%')



if __name__ == "__main__":
    # 1. Read CSV
    customers = read_csv('customers.csv')

    # 2. Validate
    errors = validate_customers(customers)


    # 3. Print report
    print_report(errors, len(customers))
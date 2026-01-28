import re


def read_csv(filename):
    curated_list = []
    with open(filename, 'r') as f:
        headers = f.readline().strip().split(",")
        for line in f:
            line = line.strip().split(",")
            curated_dictionary = dict(zip(headers, line))
            curated_list.append(curated_dictionary)

    return curated_list


def is_valid_email(email):
    if re.match(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', email):
        return True
    else:
        return False
    # return '@' in email and '.' in email.split('@')[1]


def is_valid_age(age_str):
    try:
        return 0 < int(age_str) < 120
    except ValueError:
        return False


def is_not_empty(value):
    return bool(value.strip())


def fix_email(email):
    try:
        curated_mail = ''.join(email.strip().split()).lower()
        valid = is_valid_email(curated_mail)
        return curated_mail, valid

    except TypeError:
        return email, False


def fix_age(age_str):
    try:
        curated_age = age_str.strip()
        age_int = int(float(curated_age))
        curated_age = str(age_int)
        age_valid = is_valid_age(curated_age)

        return curated_age, age_valid

    except ValueError:
        return age_str, False


def fix_name(name):
    curated_name = ''.join(name.strip()).capitalize()
    is_valid = is_not_empty(curated_name)
    return curated_name, is_valid


def fix_city(city):
    curated_city = ''.join(city.strip()).capitalize()
    is_valid = is_not_empty(curated_city)
    return curated_city, is_valid


def all_customers(persons):
    clean_customers = []
    error_customers = []
    statistics = {'total_customers': len(persons), 'fixed': 0, 'unfixable': 0}
    for customer in persons:
        fixed_city = fix_city(customer["city"])
        fixed_name = fix_name(customer["name"])
        fixed_age = fix_age(customer["age"])
        fixed_email = fix_email(customer["email"])
        if fixed_city[1] and fixed_age[1] and fixed_email[1] and fixed_name[1]:
            statistics['fixed'] += 1
            clean_customers.append({
                'name': fixed_name[0],
                'city': fixed_city[0],
                'age': fixed_age[0],
                'email': fixed_email[0]
            })
        else:
            statistics["unfixable"] += 1
            error_customers.append(customer)

    return statistics, clean_customers, error_customers


def write_csv(filename, people):
    if not people:
        return
    headers = ["name", "email", "age", "city"]
    with open(filename, 'w') as f:
        f.write(",".join(headers) + "\n")
        for customer in people:
            values = [customer[h] for h in headers]
            f.write(','.join(values) + '\n')


def validate_customers(persons):
    invalid_features = {
        'invalid_email': 0,
        'invalid_age': 0,
        'missing_name': 0,
        'missing_city': 0
    }

    for customer in persons:
        if not is_valid_email(customer["email"]):
            invalid_features['invalid_email'] += 1
        if not is_valid_age(customer["age"]):
            invalid_features['invalid_age'] += 1
        if not is_not_empty(customer["name"]):
            invalid_features['missing_name'] += 1
        if not is_not_empty(customer["city"]):
            invalid_features['missing_city'] += 1

    return invalid_features


def print_detailed_report(stats, clean_customers, error_customers):
    """Print comprehensive processing report"""
    print("=" * 50)
    print("CSV DATA CLEANER - PROCESSING REPORT")
    print("=" * 50)

    print(f"\n📊 SUMMARY:")
    print(f"   Total rows processed: {stats['total_customers']}")
    print(f"   ✅ Successfully cleaned: {stats['fixed']}")
    print(f"   ❌ Unfixable errors: {stats['unfixable']}")

    success_rate = (stats['fixed'] / stats['total_customers']) * 100
    print(f"   Success rate: {success_rate:.1f}%")

    print(f"\n📁 OUTPUT FILES:")
    print(f"   - customers_clean.csv ({stats['fixed']} rows)")
    print(f"   - customers_errors.csv ({stats['unfixable']} rows)")

    if error_customers:
        print(f"\n⚠️  UNFIXABLE RECORDS:")
        for i, customer in enumerate(error_customers[:3], 1):  # Show first 3
            print(f"   {i}. {customer['name'] or '[MISSING]'} - {customer['email']}")
        if len(error_customers) > 3:
            print(f"   ... and {len(error_customers) - 3} more")

    print("=" * 50)


import sys

if __name__ == "__main__":
    # Allow custom filenames
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'customers.csv'

    print(f"Processing {input_file}...")

    # Read CSV
    customers = read_csv(input_file)

    # Process
    stats, clean, errors = all_customers(customers)

    # Write output files
    write_csv('customers_clean.csv', clean)
    write_csv('customers_errors.csv', errors)

    # Print report
    print_detailed_report(stats, clean, errors)

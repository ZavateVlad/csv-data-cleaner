import re
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_cleaner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def read_csv(filename):
    """
    Read CSV file and convert to list of dictionaries.

    Args:
        filename(str): Path to CSV file

    Returns:
        list: List of dictionaries with header keys

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If file is empty or malformed
    """
    try:
        curated_list = []
        with open(filename, 'r') as f:
            headers = f.readline().strip().split(",")

        if not headers:
            raise ValueError("CSV file does not have any headers")

        for line_num, line in enumerate(f, start=2):
            line = line.strip().split(",")
            if len(line) != len(headers):
                logger.warning(f"Line {line_num}: Column count mismatch. Skipping.")
                continue
            curated_dictionary = dict(zip(headers, line))
            curated_list.append(curated_dictionary)

        logger.info(f"Successfully read {len(curated_list)} records from {filename}")
        return curated_list

    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        raise
    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        raise


def is_valid_email(email):
    """
    Validate email format using regex.
    Args:
        email (str): Email address to validate

    Returns:
        bool: True if email format is valid
    """
    return bool(re.match(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', email))


def is_valid_age(age_str):
    """
    Validate age between 0 and 120.

    Args:
        age_str (str) = Age as string

    Returns:
        bool: True if age is valid integer between 0 and 120
    """
    try:
        return 0 < int(age_str) < 120
    except ValueError:
        return False


def is_not_empty(value):
    """
    Check if string value is not empty after stripping whitespace.

    Args:
        value (str): String to check

    Returns:
        bool: True if string has content
    """
    return bool(value.strip())


def fix_email(email):
    """
    Clean and validate email address, removing whitespaces and converting to lowercase.

    Args:
        email (str): Raw email string

    Returns:
        tuple: The checked email string and if the string is valid or not
    """
    try:
        curated_mail = email.strip().replace(' ', '').lower()
        valid = is_valid_email(curated_mail)
        return curated_mail, valid

    except (TypeError, AttributeError):
        logger.warning(f"Invalid email type: {type(email)}")
        return email, False


def fix_age(age_str):
    """
    Clean and validates age value, while converting floats to integers.

    Args:
        age_str (str): Raw age string

    Returns:
        tuple: The checked age string and if the age is valid or not
    """
    try:
        curated_age = age_str.strip()
        age_int = int(float(curated_age))
        curated_age = str(age_int)
        age_valid = is_valid_age(curated_age)
        return curated_age, age_valid

    except ValueError:
        logger.warning(f"Invalid age format: {age_str}")
        return age_str, False


def fix_name(name):
    """
    Clean and validate name, by striping whitespaces and capitalizing each word.

    Args:
        name (str): Raw name string

    Returns:
        tuple: The checked name string and if the name is valid or not
    """
    curated_name = name.strip().title()
    is_valid = is_not_empty(curated_name)
    return curated_name, is_valid


def fix_city(city):
    """
        Clean and validate city name, by striping whitespaces and capitalizing each word.

        Args:
            city (str): Raw city string

        Returns:
            tuple: The checked city string and if the city is valid or not
        """
    curated_city = ''.join(city.strip()).capitalize()
    is_valid = is_not_empty(curated_city)
    return curated_city, is_valid


def all_customers(persons):
    """
    Process all customer records, separating clean from unfixable.

    Args:
        persons (list): List of customer dictionaries

    Returns:
        tuple: (statistics, clean_customers, error_customers)
            - statistics: dict with 'total_customers', 'fixed' and 'unfixable'
            - clean_customers: list of successfully cleaned records
            - error_customers: list of unfixable records

    """
    clean_customers = []
    error_customers = []
    statistics = {'total_customers': len(persons), 'fixed': 0, 'unfixable': 0}

    logger.info(f"Processing {len(persons)} customer records...")

    for idx, customer in enumerate(persons, start=1):
        fixed_city = fix_city(customer["city"])
        fixed_name = fix_name(customer["name"])
        fixed_age = fix_age(customer["age"])
        fixed_email = fix_email(customer["email"])

        if all([fixed_city[1], fixed_age[1], fixed_email[1], fixed_name[1]]):
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
            logger.debug(f"Record {idx} unfixable: {customer}")

    logger.info(f"Processing complete: {statistics['fixed']} cleaned, {statistics['unfixable']} errors")
    return statistics, clean_customers, error_customers


def write_csv(filename, people):
    """
    Write customer data to CSV file.

    Args:
        filename (str): Output file path
        people (list): List of customer dictionaries
    """
    if not people:
        logger.warning(f"No data to write to {filename}")
        return

    headers = ["name", "email", "age", "city"]

    try:
        with open(filename, 'w') as f:
            f.write(",".join(headers) + "\n")
            for customer in people:
                values = [customer[h] for h in headers]
                f.write(','.join(values) + '\n')

        logger.info(f"Successfully wrote {len(people)} records to {filename}")

    except Exception as e:
        logger.error(f"Error writing to {filename}: {str(e)}")
        raise


def print_detailed_report(stats, clean_customers, error_customers):
    """
    Print comprehensive processing report to console.

    Args:
        stats (dict): Processing statistics
        clean_customers (list): Successfully cleaned records
        error_customers (list): Unfixable records
    """
    print("=" * 50)
    print("CSV DATA CLEANER - PROCESSING REPORT")
    print("=" * 50)

    print(f"\nSUMMARY:")
    print(f"   Total rows processed: {stats['total_customers']}")
    print(f"Successfully cleaned: {stats['fixed']}")
    print(f"Unfixable errors: {stats['unfixable']}")

    if stats['total_customers'] > 0:
        success_rate = (stats['fixed'] / stats['total_customers']) * 100
        print(f"   Success rate: {success_rate:.1f}%")

    print(f"\nOUTPUT FILES:")
    print(f"   - customers_clean.csv ({stats['fixed']} rows)")
    print(f"   - customers_errors.csv ({stats['unfixable']} rows)")

    if error_customers:
        print(f"\nUNFIXABLE RECORDS:")
        for i, customer in enumerate(error_customers[:3], 1):
            print(f"   {i}. {customer['name'] or '[MISSING]'} - {customer['email']}")
        if len(error_customers) > 3:
            print(f"   ... and {len(error_customers) - 3} more")

    print("=" * 50)


def main():
    """Main execution function."""
    # Allow custom filenames
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'customers.csv'

    logger.info(f"Starting CSV Data Cleaner")
    logger.info(f"Input file: {input_file}")

    try:
        # Read CSV
        customers = read_csv(input_file)

        # Process
        stats, clean, errors = all_customers(customers)

        # Write output files
        write_csv('customers_clean.csv', clean)
        write_csv('customers_errors.csv', errors)

        # Print report
        print_detailed_report(stats, clean, errors)

        logger.info("Processing completed successfully")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

def are_decimal_digits_zero(number):
    # Check if the number is an integer or if the decimal part is all zeros
    return int(number) == number or int(number * 10**10) == int(number) * 10**10
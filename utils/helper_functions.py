def split_name(name):
    name_parts = name.split(" ")
    first_part = name_parts[0]
    last_part = " ".join(name_parts[1:])
    return first_part, last_part

def split_university(name):
    university_parts = name.split(",")
    first_part = university_parts[0]
    last_part = ",".join(university_parts[1:])
    return first_part, last_part

def get_serial_number(number: int):
    if number < 10:
        return "00" + str(number)
    elif number >= 10 and number < 100:
        return "0" + str(number)
    else:
        return str(number)
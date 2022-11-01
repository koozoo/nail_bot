
def print_data(data):
    res = ' '
    if data['values']:
        for i in data['values']:
           res += f'{str(i[0]).capitalize()}{i[1]}\n'
    return res


def clean_date_from_db(date: str):
    return ''.join(i for i in date.split("_")[1].replace("$", "."))


def prepare_date_for_db(date: str):
    return date.replace(".", "$")

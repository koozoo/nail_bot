def print_data(data):
    res = ' '
    if data['values']:
        for i in data['values']:
           res += f'{i[0]}{i[1]}\n'
    return res

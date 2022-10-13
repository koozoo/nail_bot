
def print_data(data):
    res = ' '
    if data['values']:
        for i in data['values']:
           res += f'{str(i[0]).capitalize()}{i[1]}\n'
    return res

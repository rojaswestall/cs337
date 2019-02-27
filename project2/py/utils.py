

def print_list(lst):
    for item in lst:
        print(item)

def print_nested_lst(lst):
    for sub_lst in lst:
        print_list(sub_lst)
        print('\n')

def flatten(lst):
    flat_list = [item for sublist in lst for item in sublist]
    return flat_list


def pmap(function, lst):
    new_lst = [function(item) for item in lst]
    return new_lst

def nested_map(function, lst):
    new_lst = [pmap(function, sublst) for sublst in lst]
    return new_lst

def unzip(lst):
    lst1, lst2 = zip(*lst)
    return lst1, lst2



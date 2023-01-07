def file_to_dict(file):
    rec = list()
    cook_book = dict()

    with open(file, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            rec.append(line)

    for i in range(len(rec)):
        if rec[i].isdigit():
            item = list()
            key = rec[i - 1]
            for j in range(1, int(rec[i]) + 1):
                ingredient_n = dict()
                ingr = rec[i + j].split(" | ")
                ingredient_n['ingredient_name'] = ingr[0]
                ingredient_n['quantity'] = int(ingr[1])
                ingredient_n['measure'] = ingr[2]
                item.append(ingredient_n)
            cook_book[key] = item
    return cook_book

def get_shop_list_by_dishes(dishes, person_count):
    shop_list = dict()
    for dish in dishes:
        for ingredient_n in cook_book[dish]:
            if ingredient_n['ingredient_name'] not in shop_list:
                shop_list[ingredient_n['ingredient_name']] = {
                        'measure': ingredient_n['measure'],
                        'quantity': ingredient_n['quantity'] * person_count
                }
            else:
                shop_list[ingredient_n['ingredient_name']]['quantity'] = (
                        shop_list[ingredient_n['ingredient_name']]['quantity']
                        + (ingredient_n['quantity'] * person_count))
    return shop_list

if __name__ == "__main__":
    file = "recipes.txt"

    cook_book = file_to_dict(file)
    print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
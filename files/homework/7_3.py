def len_files(n):
    text_files = list()

    for i in range(1, n + 1):
        filename = f"{i}.txt"
        with open(filename, encoding="utf-8") as file:
            text = [line.strip() for line in file]
            text.append(filename)
            text_files.append(text)

    text_files.sort(key=len)

    return text_files


def merging_files(text_files):
    with open('result.txt', 'w') as result:
        for text in text_files:
            result.write(text[-1] + '\n')
            result.write(str(len(text) - 1) + '\n')
            for t in text[:-1]:
                result.write(t + '\n')

    print("Результирующий файл создан")


if __name__ == '__main__':
    n = 3

    merging_files(len_files(n))
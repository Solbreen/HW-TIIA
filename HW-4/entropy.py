from collections import Counter
from math import log2

def countOfSymb(s: str):
    """
    =========================================================
    Функция для получения словаря символов и их кол-ва
    Принимает:
        s - строка с изначальным сообщением
    Возвращает:
        d - словарь с ключами символами и их кол-вом
    =========================================================
    """
    d = dict()
    l = (s.replace(" ", "")).lower()
    for i in l:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1
    return d

def probability(s: str):
    """
    =========================================================
    Функция для получения словаря символов и их вероятности
    Принимает:
        s - строка с изначальным сообщением
    Возвращает:
        d - словарь с ключами символами и их вероятностью
    =========================================================
    """
    d = dict()
    l = (s.replace(" ", "")).lower()
    length = len(l)
    for i in l:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1
    for i in d.keys():
        d[i] = d[i]/length
    return d

def coding(d):
    """
    =========================================================
    Создает словарь с кодами Фано для заданного набора символов
    Принимает:
        d - Словарь символов
    Возвращает:
        Словарь, где ключи - символы, а значения - их коды
    =========================================================
    """
    d_sorted = Counter(d)
    sorted_l = sorted(d_sorted, key=d_sorted.get, reverse=True)

    code = {}
    fanoCoding(d_sorted, sorted_l, code, "", 0, len(sorted_l))

    return code

def fanoCoding(d, symbols, code, prefix, start, end):
    """
    =========================================================
    Функция для создания кода Фано
    Принимает:
        d - Сортированный словарь с вероятностями
        symbols - Список символов СОРТИРОВАННЫЙ КАК И СЛОВАРЬ!
        code - Словарь с кодами Фано
        prefix - Префикс для кода
        start - Начальный индекс
        end - Конечный индекс
    =========================================================
    """
    if start == end or end - start == 1:
        code[symbols[start]] = prefix
        return
    elif len(symbols[start:end]) == 2:
        code[symbols[start]] = prefix + "1"
        code[symbols[end-1]] = prefix + "0"
        return 

    sum = 0
    for i in symbols[start:end]:
        sum += d[i]

    mid = start
    left = 0
    for i in symbols[start:end]:
        left += d[i]
        if left < (sum - left) and abs(left - abs(sum-left)) >= 0.0001:
            mid += 1
        elif abs(left - abs(sum-left)) < 0.0001:
            mid += 1
            break
        else:
            if abs(sum / 2 - left) < abs(sum /2 - left + d[i]):
                mid += 1
                break
            else:
                break

    fanoCoding(d, symbols, code, prefix + "1", start, mid)
    fanoCoding(d, symbols, code, prefix + "0", mid, end)

def entropy(d):
    """
    ==========
    Вычисляем энтропию
    Принимаем:
        d - словарь с вероятностями
    Возвращаем:
        h - энтропию
    ==========
    """
    h = 0
    for i in d.values():
        h -= i * log2(i)
    return h

def avrLen(code, d):
    sum = 0
    for i in d.keys():
        sum += d[i]*len(code[i])
    return sum

def compress(s, code):
    """
    ===============================================
    Сжимает текст, закодированный по условию Фано
    Принимает:
        s - текст для сжатия
        code - cловарь с кодами Фано
    Возвращает:
        Сжатый текст в виде двоичной строки
    ===============================================
    """

    compressed = ""
    for symbol in s:
        compressed += code[symbol]

    return compressed





def main():
    print()
    s = input("Введите текст: ")
    p = probability(s)
    SymCount = countOfSymb(s)
    fc = coding(SymCount)
    print()
    print("Коды Фано для символов: ")
    print(fc)
    print()
    print("Энтропия H(x) = ", entropy(p))
    print()
    print("Максимально возможное сжатие: ", avrLen(fc, p) / entropy(p))
    print()
    print("Сжатый текст: ")
    print(compress(s.replace(" ", "").lower(), fc))


if __name__ == '__main__':
    main()
#=========================================================================
import pandas

#=========================================================================
# Для выписывания всех слов, начиная с данного узла
def print_branch_words(a_branch, a_word=""):
    #Дальше некуда, выводим
    if a_branch == []:
        return []
    #если это слово - выводим
    if a_branch[0][1] == True:
        return [a_word + a_branch[0][0]] +\
               print_branch_words(a_branch[1], a_word + a_branch[0][0]) +\
               print_branch_words(a_branch[2], a_word)
    else:
        return print_branch_words(a_branch[1], a_word + a_branch[0][0]) +\
               print_branch_words(a_branch[2], a_word)

#=========================================================================
# Инициализация выписывания всех слов
def init_print_branch_words(a_branch, a_word = ""):
    # список пуст и слова нет
    if a_branch == [] and a_word == "":
        return []
    # список пуст: мы ввели полное слово, больше подобных слов нет.
    elif a_branch == []:
        return [a_word]
    #Всё в порядке, выполняем основную функцию
    else:
        print_branch_words(a_branch, a_word)

#=========================================================================
# Для поиска подходящих слов
def find_words(a_value, a_branch, a_prefix = ""):
    #слово пустое, выводим всё что есть дальше
    if a_value == "":
        return print_branch_words(a_branch, a_prefix)
    #массив закончился
    if a_branch == []:
        return []
    #нашли букву
    if a_branch[0][0] == a_value[0]:
        if len(a_value) > 1:
            #Ещё полно букв для поиска, продолжаем
            return find_words(a_value[1:], a_branch[1], a_prefix + a_value[0])
        else:
            #Готово. Это была последняя буква. Засовываем остаточное дерево с дерево с найденным кортежем
            #(вдруг он слово заканчивает: человек ввёл целое слово)
            return print_branch_words([a_branch[0], a_branch[1], []], a_prefix)
    #не нашли букву
    else:
        return find_words(a_value, a_branch[2], a_prefix)

#=========================================================================
# Для добавления новых слов
def add(a_value, a_branch, a_prefix = ""):
    #закончилось слово (слово уже есть)
    if a_value == "":
        return a_branch
    #дерево закончилось, добавляем
    if a_branch == []:
        #последняя буква - ставим в кортеж ИСТИНА
        if len(a_value) == 1:
            return [(a_value[0], True), [], []]
        #не последняя буква - ставим в кортеж ЛОЖЬ
        else:
            return [(a_value[0], False), add(a_value[1:], [], a_prefix + a_value[0]), []]
    #нашли букву
    if a_branch[0][0] == a_value[0]:
        # последняя буква - ставим в кортеж ИСТИНА
        if len(a_value) == 1:
            return [(a_value[0], True), a_branch[1], a_branch[2]]
        else:
            return [a_branch[0], add(a_value[1:], a_branch[1], a_prefix + a_value[0]), a_branch[2]]

    #не нашли букву
    else:
        return [a_branch[0], a_branch[1], add(a_value, a_branch[2], a_prefix)]

#=========================================================================
#MAIN
#=========================================================================
TREE = []

for word in pandas.read_csv("dictionaire_big.csv", sep=","):
   TREE = add(word, TREE)


#Это были тестовые слова
TREE = add("artistic", TREE)
TREE = add("art", TREE)
TREE = add("ball", TREE)
TREE = add("arctang", TREE)
TREE = add("arctang", TREE) #!
TREE = add("arcticulate", TREE)
TREE = add("archive", TREE)
TREE = add("argentum", TREE)

print(find_words("s", TREE))
#=========================================================================

''' Не функциональная херота для тестов
some = ""
while True:
    print("(E)xit, (F)ind, (A)dd")
    some = input()

    if some == "E" or some =="e":
        break

    elif some == "A" or some == "a":
        some = input("Add new word: ")
        TREE = add(some, TREE)
        continue

    elif some == "F" or some =="f":
        some = input("Searching for words: ")
        print(find_words(some, TREE))
        continue

    else:
        print("Unknown command")
        continue
'''
#=========================================================================



import re
from collections import defaultdict
import csv
import time

def word_frequency_from_file(filename):
    # Открыть файл для чтения
    with open(filename, "r", encoding="utf-8") as file:
        # Прочитать текст из файла
        text = file.read()

    # Привести весь текст к нижнему регистру
    text = text.lower()

    # Разделить текст на слова
    words = re.findall(r"\w+", text)  # используем регулярное выражение для разделения

    # Создать пустой словарь для подсчета частоты слов
    word_counts = defaultdict(int)

    # Подсчитать частоту каждого слова
    for word in words:
        word_counts[word] += 1

    return word_counts

def word_frequency_to_csv(filename, word_counts):
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Открыть файл для записи
    with open(filename, "w", newline="", encoding="utf-8") as file:
        # Записать заголовок в файл
        writer = csv.writer(file)
        writer.writerow(["Слова", "Количество"])

        # Записать каждое слово и его частоту в файл
        for word, count in sorted_word_counts:
            writer.writerow([word, count])

filename_input = "Herbert_Dyuna-Hroniki-Dyuny_1_Dyuna_RuLit_Me.txt"
filename_output = "out_put_1.csv"

start_time = time.time()
frequency = word_frequency_from_file(filename_input)
word_frequency_to_csv(filename_output, frequency)
print("Execution time:", time.time() - start_time)

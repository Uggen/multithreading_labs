import threading
import random
import time


class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork, stop_event, eat_count, eat_count_lock):
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.stop_event = stop_event
        self.eat_count = eat_count
        self.eat_count_lock = eat_count_lock

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(random.uniform(1, 5))  # Размышление
            self.dine()

    def dine(self):
        fork1, fork2 = self.left_fork, self.right_fork

        while not self.stop_event.is_set():
            self.print_status("размышление")
            fork1.acquire(True)
            self.print_status("взял левую вилку")
            locked = fork2.acquire(False)
            if locked:
                self.print_status("взял правую вилку")
                break  # Если вторая вилка доступна, начинаем есть
            fork1.release()
            self.print_status("отдал вилки")
            fork1, fork2 = fork2, fork1
        else:
            return

        self.dining()
        fork2.release()
        fork1.release()

    def dining(self):
        self.print_status("поел")
        time.sleep(random.uniform(1, 5))
        with self.eat_count_lock:
            self.eat_count[self.index] += 1
        self.print_status("отдал вилки")

    def print_status(self, status):
        print(f"{self.index + 1} философ | {status}")


class Fork:
    def __init__(self, index):
        self.lock = threading.Lock()
        self.index = index

    def acquire(self, blocking=True):
        return self.lock.acquire(blocking)

    def release(self):
        return self.lock.release()


def main():
    stop_event = threading.Event()
    forks = [Fork(i) for i in range(5)]
    eat_count = [0] * 5
    eat_count_lock = threading.Lock()
    philosophers = [Philosopher(i, forks[i], forks[(i + 1) % 5], stop_event, eat_count, eat_count_lock) for i in range(5)]

    for philosopher in philosophers:
        philosopher.start()

    start_time = time.time()  # Замеряем время старта программы
    time.sleep(10)  # Устанавливаем время работы программы
    stop_event.set()  # Устанавливаем событие для завершения программы

    for philosopher in philosophers:
        philosopher.join()  # Ждем завершения всех потоков

    end_time = time.time()  # Замеряем время окончания программы

    # print("Программа завершена.")
    total_time = end_time - start_time
    print(f"Время выполнения программы: {total_time} секунд.")

    print("Количество приемов пищи для каждого философа:")
    for i in range(5):
        print(f"Философ {i + 1}: {eat_count[i]} раз")

if __name__ == "__main__":
    main()

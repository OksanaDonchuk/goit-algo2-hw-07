import random
import time
from functools import lru_cache
from typing import List, Tuple

# Масив для кешування в @lru_cache
array_reference = []

# Функція кешованого підрахунку суми
@lru_cache(maxsize=1000)
def range_sum_with_cache_functools(array_id: int, L: int, R: int) -> int:
    """Обчислює суму елементів на відрізку [L, R] з кешем."""
    return sum(array_reference[L:R+1])

# Використання кешу у функції range_sum
def range_sum_with_cache(array: List[int], L: int, R: int) -> int:
    """Обчислює суму елементів масиву на відрізку [L, R] з кешем."""
    global array_reference
    array_reference = array  # Оновлюємо посилання на масив
    return range_sum_with_cache_functools(id(array), L, R)

# Функція оновлення елементу з очищенням кешу
def update_with_cache(array: List[int], index: int, value: int) -> None:
    """Оновлює значення елемента масиву та очищає кеш."""
    if not 0 <= index < len(array):
        raise IndexError("Індекс виходить за межі масиву")
    
    array[index] = value
    range_sum_with_cache_functools.cache_clear()  # Очищуємо кеш, бо масив змінився

# Функція підрахунку суми БЕЗ кешу
def range_sum_no_cache(array: List[int], L: int, R: int) -> int:
    """Обчислює суму елементів на відрізку [L, R] без кешу."""
    return sum(array[L:R+1])

# Функція оновлення БЕЗ кешу
def update_no_cache(array: List[int], index: int, value: int) -> None:
    """Оновлює елемент масиву без використання кешу."""
    if not 0 <= index < len(array):
        raise IndexError("Індекс виходить за межі масиву")
    array[index] = value

# Генерація тестових даних
N = 100_000  # Розмір масиву
Q = 50_000  # Кількість запитів
array = [random.randint(1, 100) for _ in range(N)]
queries: List[Tuple[str, int, int]] = []

for _ in range(Q):
    if random.random() < 0.9:  # 90% Range, 10% Update
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 100)
        queries.append(('Update', index, value))

# Підрахунок кількості запитів
range_queries = sum(1 for query in queries if query[0] == 'Range')
update_queries = sum(1 for query in queries if query[0] == 'Update')

print(f"Кількість Range-запитів: {range_queries}")
print(f"Кількість Update-запитів: {update_queries}")

# Виконання БЕЗ кешу
start_time_no_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array, query[1], query[2])
    elif query[0] == 'Update':
        update_no_cache(array, query[1], query[2])
end_time_no_cache = time.time()

# Виконання З КЕШЕМ
start_time_with_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(array, query[1], query[2])
    elif query[0] == 'Update':
        update_with_cache(array, query[1], query[2])
end_time_with_cache = time.time()

# Вивід результатів
execution_time_no_cache = end_time_no_cache - start_time_no_cache
execution_time_with_cache = end_time_with_cache - start_time_with_cache

print(f"Час виконання без кешування: {execution_time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {execution_time_with_cache:.2f} секунд")

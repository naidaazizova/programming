import pathlib
import typing as tp
import random
import time
import multiprocessing
T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i + n] for i in range(0, len(values), n)]

     #[values[i:i + n] - создаем срез списка от индекса i до i+n, чтобы
     #получить подсписки фиксированной длины n

     #range(0, len(values), n) - генерируем индексы, начиная с 0 и
     #увеличивая на n до конца списка values
    pass


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, _ = pos
    return grid[row]

    pass


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    _, col = pos
    return [grid[row][col] for row in range(len(grid))]
    pass


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3
    #Мы определяем к какому 3х3 блоку принадлежит pos.

    #row // 3 - делит номер строки на 3 и округляет вниз, чтобы определить,
    # в каком списке из 3 строк находится данная строка
    #умножив на 3, мы получаем индекс первой строки столбца

    #точно также делаем и для столбца

    return [grid[r][c]
            for r in range(block_row, block_row + 3)
            for c in range(block_col, block_col + 3)]
    #Внешний цикл for r in range(block_row, block_row + 3) проходит по трем строкам блока
    #Внутренний цикл for c in range(block_col, block_col + 3) проходит по трем столбцам блока
    #Мы собираем значения в одномерный список, обращаясь к элементам сетки grid[r][c]
    pass


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    #enumarate позволяет пройтись по каждой строке нашей сетки grid
    for row, row_cont in enumerate(grid):
        for col, cell in enumerate(row_cont):
            if cell == ".":
                return row, col
    return None
    pass


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    possible_values = set("123456789")
    row_values = set(get_row(grid, pos))
    col_values = set(get_col(grid, pos))
    block_values = set(get_block(grid, pos))
    use_values = row_values | col_values | block_values
    return possible_values - use_values
    pass


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if not pos:
        return grid  #все позиции заполнены, поэтому возвращаем текущую сетку, которая уже является решением
    row, col = pos #извлекаем строку и столбец из найденной пустой позиции
    for value in find_possible_values(grid, pos):  #перебираем все значения, которые могут быть размещены в pos,
        # вызывая функцию find_possible_values
        grid[row][col] = value #помещаем текущее значение value в пустую позицию
        solution = solve(grid) #рекурсивно вызываем функцию, чтобы дорешать судоку уже с обновленной сеткой
        if solution:
            return solution #если рекурсивный вызов вернул решение, возвращаем это решение
        grid[row][col] = "." #откатываем изменения, устанавливая ячейку обратно в пустое состояние
    return None  #решений нет для судоку


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    # эта функция проверяет, является ли группа(список строк, который представляет собой
    # либо строку, либо столбец, либо блок 3х3 судоку) допустимой (то есть имеет уникальные значения
    # от 1 до 9, игнорируя пустые клетки)
    def valid_group(group: tp.List[str]) -> bool:
        elements = [x for x in group if x != "."]  #игнорируем пустые клетки
        return (
                len(elements) == len(set(elements)) #проверяем, что все заполненные значения уникальны,
                # сравнивая длину списка с длиной множества(в множестве нет дубликатов)
                and all(e in "123456789" for e in elements))

    #проверяем строки
    for row in solution:
        if not valid_group(row):
            return False

    #проверяем столбцы
    for col in range(9):
        column = [solution[row][col] for row in range(9)]
        if not valid_group(column):
            return False

    #проверяем блоки 3x3
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block = [solution[r][c]
                for r in range(block_row, block_row + 3)
                for c in range(block_col, block_col + 3)]
            if not valid_group(block):
                return False
    return True
    pass


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    #создаем пустую сетку
    grid = [["." for _ in range(9)] for _ in range(9)]
    #находим решение для пустой сетки
    solution = solve(grid)
    if not solution:
        return grid  #если решение не найдено, возвращаем пустую сетку
    #копируем решение
    grid = [row[:] for row in solution]
    N = max(0, min(N, 81)) # ограничиваем N допустимыми значениями
    positions = [(row, col) for row in range(9) for col in range(9)] #создается список всех возможных позиций клеток в сетке (от (0, 0) до (8, 8)),
    # который затем перемешивается с помощью random.shuffle.
    random.shuffle(positions)
    for i in range(81 - N): #в цикле удаляются клетки, пока не останется заданное количество заполненных клеток.
        #для каждой итерации берется позиция из перемешанного списка и соответствующая клетка в сетке устанавливается в .
        row, col = positions[i]
        grid[row][col] = "."
    return grid #возвращается финальная сетка судоку с заданным количеством заполненных клеток
    pass

def solve_puzzle(filename: str) -> None:
    """
    Прочитаем пазл из файла, решим его и выведем результат
    """
    try:
        grid = read_sudoku(filename)
        print(f"Исходный пазл из файла {filename}:") #печатается исходная сетка и отображается с помощью функции display.
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Пазл из файла {filename} не может быть решен\n")
        else:
            print(f"Решение для файла {filename}:")
            display(solution)
            if check_solution(solution):
                print("Решение верноe\n")
            else:
                print("Решение неверноe\n")
    except FileNotFoundError:
        print(f"Файл {filename} не найден\n")
    except ValueError as error:
        print(f"Ошибка в файле {filename}: {error}\n")

def run(filename: str) -> None:
    """
    Решаем пазл и выводим время его выполнения
    """
    grid = read_sudoku(filename)
    start_time = time.time() #сохраняем текущее время, чтобы позже измерить время выполнения
    solution = solve(grid) #вызываем функция solve, чтобы найти решение для загруженного пазла
    end_time = time.time() #сохраняем текущее время после завершения решения
    #если решение найдено, выводится время, затраченное на решение.В противном случае
    # выводится сообщение о том, что решение не найдено
    if solution:
        print(f"{filename}: {end_time - start_time:.6f} секунд")
    else:
        print(f"{filename}: Решение не найдено")


if __name__ == "__main__":
    #Этот блок выполняется только если файл запускается как основной модуль, а не импортируется.
    # Определяется список файлов с пазлами.
    puzzle_files = ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]
    processs = []
    for file in puzzle_files: #Для каждого файла создается новый процесс,
        # который запускает функцию run. Процессы добавляются в список processs.
        process = multiprocessing.Process(target=run, args=(file,))
        processs.append(process)
        process.start()
    #После запуска всех процессов основной поток ждет их завершения с помощью метода join.
    for process in processs:
        process.join()
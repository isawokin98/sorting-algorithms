import copy as c
import enum as e
import random as r
import typing as t
import time as ti

import tabulate as tab


def swap(buffer: t.List[int], i: int, j: int) -> None:
    """Swaps two elements in a list"""
    temp = buffer[j]
    buffer[j] = buffer[i]
    buffer[i] = temp


def selection_sort_iterative(buffer: t.List[int]) -> None:
    """In-place selection sort using iteration"""
    for i in reversed(range(len(buffer))):

        # get largest el of buffer with index <= i
        idx_largest = get_idx_of_largest_element(buffer, i)
        swap(buffer, i, idx_largest)


def selection_sort_recursive(buffer: t.List) -> None:
    """In-place selection sort using iteration"""
    starting_id = len(buffer) - 1

    def rec(i: int) -> None:
        """Inline function running recursion"""
        if i < 0:
            return

        idx_largest = get_idx_of_largest_element(buffer, i)
        swap(buffer, i, idx_largest)

        rec(i-1)

    rec(starting_id)


def get_idx_of_largest_element(buffer: t.List, end_idx: int) -> int:
    """Gets index of largest element with an index < end_idx + 1"""
    idx_largest = end_idx
    largest = buffer[idx_largest]
    for j in reversed(range(end_idx+1)):
        if largest < buffer[j]:
            idx_largest = j
            largest = buffer[j]

    return idx_largest


def run_sorting_fn_and_get_average_time(
        sorting_fn: t.Callable,
        buffer: t.List,
        times_to_run: int = 10
) -> str:

    copy_buffer = c.copy(buffer)
    sorting_fn(copy_buffer)

    assert copy_buffer == sorted(buffer)

    times_taken = []
    for i in range(times_to_run):
        copied_buffer = c.copy(buffer)

        start = ti.time()
        sorting_fn(copied_buffer)
        end = ti.time()
        time_taken = end-start

        times_taken.append(time_taken)
    return format(sum(times_taken) / times_to_run, '.17f')


def build_in_sort_wrapper(arr):
    """Wrapper around built in .sort() method"""
    arr.sort()


class DatasetTypeEnum(e.Enum):
    RANDOM = "RANDOM"
    SORTED = "SORTED"
    REVERSE_SORTED = "REVERSE_SORTED"
    ALL_ELEMENTS_EQUAL = "ALL_ELEMENTS_EQUAL"


def run_on_different_data_set_types(
        sorting_fn: t.Callable,
        data_set_type: DatasetTypeEnum,
        input_length: int
) -> str:
    random_data = [r.randint(-10000, 10000) for i in range(input_length)]

    data_set_type_to_data_set = {
        DatasetTypeEnum.RANDOM: random_data,
        DatasetTypeEnum.SORTED: sorted(random_data),
        DatasetTypeEnum.REVERSE_SORTED: sorted(random_data, reverse=True),
        DatasetTypeEnum.ALL_ELEMENTS_EQUAL: [random_data[0] for i in range(input_length)]
    }

    data_set = data_set_type_to_data_set[data_set_type]

    try:
        return run_sorting_fn_and_get_average_time(sorting_fn, data_set)
    except RecursionError:
        return "Max Recursion Error"


def print_table() -> None:
    """Prints table of execution times for sorting algorithms"""
    rows = []
    input_sizes = [0, 1, 2, 10, 100, 1000, 10000]
    for dataset_type in DatasetTypeEnum:
        for input_size in input_sizes:
            rows.append(
                [
                    dataset_type.name, input_size,
                    run_on_different_data_set_types(selection_sort_iterative, dataset_type, input_size),
                    run_on_different_data_set_types(selection_sort_recursive, dataset_type, input_size),
                    run_on_different_data_set_types(build_in_sort_wrapper, dataset_type, input_size)
                ]
            )

    table = tab.tabulate(
        rows,
        headers=["Dataset type", "Input Size", "Selection Sort (iterative)",
                 "Selection Sort (recursive)", "Built-in sorted() Method"]
    )
    print(table)


if __name__ == "__main__":
    print_table()

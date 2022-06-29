import copy
import enum as e
import random as r
import typing as t
import time as ti
import numpy as np
import tabulate as tab


def swap(buffer: np.array, i: int, j: int) -> None:
    """Swaps two elements in a list"""
    temp = buffer[j]
    buffer[j] = buffer[i]
    buffer[i] = temp


def selection_sort_iterative(buffer: np.array) -> None:
    """In-place selection sort using iteration"""
    for i in reversed(range(len(buffer))):

        # get largest el of buffer with index <= i
        idx_largest = get_idx_of_largest_element(buffer, i)
        swap(buffer, i, idx_largest)


def selection_sort_recursive(buffer: np.array) -> None:
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


def insertion_sort_iterative(buffer: np.array) -> None:
    """In-place insertion sort using iteration"""

    for i in range(1, len(buffer)):
        j = i
        while j > 0 and buffer[j] < buffer[j-1]:
            swap(buffer, j, j-1)
            j -= 1


def insertion_sort_recursive(buffer: np.array) -> None:
    """In-place insertion sort using recursion"""

    def sort(i: int):
        if i == len(buffer):
            return

        j = i
        while j > 0 and buffer[j] < buffer[j-1]:
            swap(buffer, j, j-1)
            j -= 1

        sort(i + 1)

    sort(0)


def get_idx_of_largest_element(buffer: np.array, end_idx: int) -> int:
    """Gets index of largest element with an index < end_idx + 1"""
    idx_largest = end_idx
    largest = buffer[idx_largest]
    for j in reversed(range(end_idx+1)):
        if largest < buffer[j]:
            idx_largest = j
            largest = buffer[j]

    return idx_largest


def merge_sort_recursive(buffer: np.array) -> None:
    """In place recursive merge sort"""

    def sort(start, end) -> None:
        if end - start < 2:
            return

        mid = int((end + start) / 2)

        sort(start, mid)
        sort(mid, end)
        merge(buffer, start, end, mid)

    sort(0, len(buffer))


def merge_sort_iterative(buffer: np.array) -> None:
    """In place iterative merge sort"""

    starting_merge_len = 2

    while starting_merge_len <= len(buffer):
        start = 0
        while start < len(buffer):
            end = min(start + starting_merge_len, len(buffer))
            mid = min(start + int(starting_merge_len/2), len(buffer))

            merge(buffer, start, end, mid)

            start = end

        starting_merge_len *= 2

    if starting_merge_len/2 < len(buffer):
        merge(buffer, 0, len(buffer), int(starting_merge_len/2))


def merge(buffer, start, end, mid: int) -> np.array:
    """In place merge intervals [start, mid), [mid, end)"""

    # temporarily use this array for merging, will copy back into buffer
    merged_arr = np.array([0 for i in range(len(buffer))])

    i = start
    j = mid
    k = start
    while i < mid and j < end:
        if buffer[i] < buffer[j]:
            merged_arr[k] = buffer[i]
            i += 1
            k += 1

        else:
            merged_arr[k] = buffer[j]
            j += 1
            k += 1
    # handle remaining parts of arrays
    while i < mid:
        merged_arr[k] = buffer[i]
        i += 1
        k += 1
    while j < end:
        merged_arr[k] = buffer[j]
        j += 1
        k += 1

    # copy back into original buffer
    for i in range(start, end):
        buffer[i] = merged_arr[i]


class Heap:
    """Class representing a MinHeap"""
    def __init__(self, buffer):
        self.heap = self._build_heap(buffer)

    def sort(self):

        sorted_heap = []
        for idx in range(len(self.heap)):
            smallest_in_heap = self.delete()
            sorted_heap.append(smallest_in_heap)

        self.heap = sorted_heap

    def _build_heap(self, buffer):
        heap = []

        for el in buffer:
            self._insert(heap, el)

        return heap

    def _insert(self, heap, el):
        heap.append(el)

        idx = len(heap) - 1

        while idx > 0:
            parent_idx = int((idx - 1) / 2)

            if heap[idx] < heap[parent_idx]:
                self._swap(heap, idx, parent_idx)
                idx = parent_idx
            else:
                break

    def delete(self):

        deleted_el = self.heap[0]
        self._swap(self.heap, 0, len(self.heap) - 1)
        self.heap.pop()

        idx = 0
        while idx < len(self.heap):
            left_child_idx = (idx + 1) * 2 - 1
            right_child_idx = (idx + 1) * 2

            smaller_child_idx = left_child_idx
            if left_child_idx > len(self.heap) - 1:
                break
            if right_child_idx < len(self.heap):
                if self.heap[right_child_idx] < self.heap[left_child_idx]:
                    smaller_child_idx = right_child_idx

            if self.heap[smaller_child_idx] < self.heap[idx]:
                self._swap(self.heap, smaller_child_idx, idx)
                idx = smaller_child_idx
            else:
                break

        return deleted_el

    def _swap(self, heap, idx1, idx2):

        temp = heap[idx1]
        heap[idx1] = heap[idx2]
        heap[idx2] = temp


def heap_sort(buffer: np.array) -> None:
    """In place heap sort"""
    heap = Heap(buffer)
    heap.sort()

    for i in range(len(buffer)):
        buffer[i] = heap.heap[i]


def run_sorting_fn_and_get_average_time(
        sorting_fn: t.Callable,
        buffer: np.array,
        times_to_run: int = 10
) -> str:

    copy_buffer = buffer.copy()
    sorting_fn(copy_buffer)

    assert np.array_equal(copy_buffer, np.sort(buffer)), f"\n {copy_buffer} \n {np.sort(buffer)}"

    times_taken = []
    for i in range(times_to_run):
        copied_buffer = buffer.copy()

        start = ti.time()
        sorting_fn(copied_buffer)
        end = ti.time()
        time_taken = end-start

        times_taken.append(time_taken)
    return format(sum(times_taken) / times_to_run, '.17f')


def build_in_sort_wrapper(arr: np.array):
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
        DatasetTypeEnum.RANDOM: np.array(random_data),
        DatasetTypeEnum.SORTED: np.sort(np.array(random_data)),
        DatasetTypeEnum.REVERSE_SORTED: np.sort(np.array(random_data))[::-1],
        DatasetTypeEnum.ALL_ELEMENTS_EQUAL: np.array([random_data[0] for i in range(input_length)])
    }

    data_set = data_set_type_to_data_set[data_set_type]

    try:
        return run_sorting_fn_and_get_average_time(sorting_fn, data_set)
    except RecursionError:
        return "Max Recursion Error"


def print_table() -> None:
    """Prints table of execution times for sorting algorithms"""
    rows = []
    input_sizes = [0, 1, 2, 10, 100]
    for dataset_type in DatasetTypeEnum:
        for input_size in input_sizes:
            rows.append(
                [
                    dataset_type.name, input_size,
                    run_on_different_data_set_types(selection_sort_iterative, dataset_type, input_size),
                    run_on_different_data_set_types(selection_sort_recursive, dataset_type, input_size),
                    run_on_different_data_set_types(insertion_sort_iterative, dataset_type, input_size),
                    run_on_different_data_set_types(insertion_sort_recursive, dataset_type, input_size),
                    run_on_different_data_set_types(build_in_sort_wrapper, dataset_type, input_size),
                    run_on_different_data_set_types(merge_sort_recursive, dataset_type, input_size),
                    run_on_different_data_set_types(merge_sort_iterative, dataset_type, input_size),
                    run_on_different_data_set_types(heap_sort, dataset_type, input_size)
                ]
            )

    table = tab.tabulate(
        rows,
        headers=[
            "Dataset type", "Input Size", "Selection Sort (iterative)",
             "Selection Sort (recursive)", "Insertion Sort (iterative)",
             "Insertion Sort (recursive)", "Built-in sorted() Method",
              "Merge Sort (recursive)", "Merge Sort (iterative)", "Heap Sort"
         ]
    )
    print(table)


if __name__ == "__main__":
    print_table()

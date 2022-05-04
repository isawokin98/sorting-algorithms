import random as r


def selection_sort_iterative(arr):
    """
              i
    1 2 3 5 9 4
          j
    """
    i = len(arr) - 1
    while i >= 0:
        j = len(arr) - 1
        while j > i and arr[j] >= arr[i]:
            j -= 1

        temp = arr[j]
        arr[j] = arr[i]
        arr[i] = temp
        i = j - 1


def selection_sort_recursive(arr):
    starting_id = len(arr) - 1

    def rec(i):
        if i < 0:
            return
        j = len(arr) - 1
        while j > i and arr[j] >= arr[i]:
            j -= 1

        temp = arr[j]
        arr[j] = arr[i]
        arr[i] = temp
        rec(j-1)

    rec(starting_id)

arr = [r.randint(-1000, 10000) for i in range(10)]
print(arr)
ans = selection_sort_recursive(arr)

print(arr == sorted(arr), arr)

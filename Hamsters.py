def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def max_hamsters(S, C, hamsters):
    left, right = 0, C
    result = 0

    while left <= right:
        k = (left + right) // 2

        if k == 0:
            left = 1
            continue

        foods = [h + g * (k - 1) for h, g in hamsters]
        foods = merge_sort(foods)
        total = sum(foods[:k])

        if total <= S:
            result = k
            left = k + 1
        else:
            right = k - 1

    return result

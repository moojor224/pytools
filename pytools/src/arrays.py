def arrMap(arr, callback):
    """python implementation of javascript's Array.prototype.map"""
    return [callback(arr[idx], idx, arr) for idx in range(len(arr))]


def interleaveArrays(fill, *arrays):
    """interleaves arrays with an optional hole filler"""
    if fill is not None:
        arrmax = max(arrMap(arrays, lambda s, idx, arr: len(s)))
        arrays = arrMap(
            arrays, lambda i, idx, arr: i + [None for _ in range(arrmax - len(i))]
        )
    result = []
    while True in arrMap(arrays, lambda arr, idx, _: True if len(arr) > 0 else False):
        for arr in arrays:
            if len(arr) > 0:
                result.append(arr.pop(0))
        pass
    return result


def rectangle(size, fill=None):
    height = round((size ** (0.5)) + 0.5)
    width = height
    while height * width - width >= size:
        height -= 1
    arr = [[fill for e in range(width)] for i in range(height)]
    return arr

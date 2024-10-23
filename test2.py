import random

def shuffle_subarray(arr, start, end):
    if start < 0 or end >= len(arr) or start > end:
        raise ValueError("Chỉ số không hợp lệ")
    
    subarray = arr[start:end+1]
    
    random.shuffle(subarray)

    arr[start:end+1] = subarray
    
    return arr

# Ví dụ sử dụng
arr = [1,2,3,4]
start = 0
result = shuffle_subarray(arr, start, len(arr)-1)
print(result)

"Some random utils"

def countin(iterable, searchedobj):
    "How many times does an object appear in an iterable?"
    count = 0
    for obj in iterable:
        if obj == searchedobj:
            count += 1
    return count

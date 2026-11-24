
import sys

def get_list():
    result = []
    for n in [1, 2, 3]:
        print("making", n)
        result.append(n)
    return result


def get_gen():
    for n in [1, 2, 3]:
        print("making", n)
        yield n


# print("LIST")
# for x in get_list():
#     print("got", x)
#
# print("GENERATOR")
# for x in get_gen():
#     print("got", x)

#
# squares_list = [n * n for n in range(1_000_000)]
# squares_gen = (n * n for n in range(1_000_000))
#
# print(sys.getsizeof(squares_list))
# print(sys.getsizeof(squares_gen))

def even_numbers(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n
print("EVEN NUMBERS " , list(even_numbers( [1, 2, 3, 4, 5, 6])))
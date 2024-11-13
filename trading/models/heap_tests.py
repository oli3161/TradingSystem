# from ..models import *
from client import Client
from order import Order
from heaps import MinOrderHeap, MaxOrderHeap


# Example usage:
# Assuming an instance of Client class is available
client = Client("ClientName")  # Placeholder client instantiation

# Creating orders
order1 = Order("AAPL", 100, 10, "2021-01-01", client)
order2 = Order("AAPL", 200, 5, "2021-01-02", client)
order3 = Order("AAPL", 100, 15, "2021-01-03", client)
order4 = Order("AAPL", 200, 5, "2021-01-06", client)

# Using MinOrderHeap
# min_heap = MinOrderHeap()
# min_heap.push(order1)
# min_heap.push(order2)
# min_heap.push(order3)
# print("MinOrderHeap:", min_heap)  # Orders sorted by price and FIFO for duplicates
# print("MinOrderHeap Pop:", min_heap.pop().order_date)
# print("MinOrderHeap after Pop:", min_heap)

# Using MaxOrderHeap
max_heap = MaxOrderHeap()
max_heap.push(order1)
max_heap.push(order2)
max_heap.push(order3)
max_heap.push(order4)
print("MaxOrderHeap:", max_heap)  # Orders sorted by descending price and FIFO for duplicates
print("MaxOrderHeap Pop:", max_heap.pop().order_date)
print("MaxOrderHeap after Pop:", max_heap)
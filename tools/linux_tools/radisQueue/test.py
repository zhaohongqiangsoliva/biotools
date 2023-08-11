from redis_queue import Queue

q = Queue("queuefile", host="192.168.77.45", port=6379, password='123942')
print(q.put_nowait("sssss"))
# print(q.get())
# print(q.Full())
m = Queue("queuefile", host="192.168.77.45", port=6379, password='123942')
print(m.get())
# try:
print(m.get)
# except Exception as e:
#     print(e)
print(q.put_nowait("sssss"))
print(m.get())
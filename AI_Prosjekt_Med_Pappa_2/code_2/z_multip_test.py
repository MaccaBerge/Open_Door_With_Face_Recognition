import multiprocessing


def make_process(num: int | float) -> int | float:
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=square, args=(num, queue))
    process.start()
    process.join()
    return queue.get()


def square(num: int | float, queue: multiprocessing.Queue) -> int | float:
    result = num * num
    queue.put(result)
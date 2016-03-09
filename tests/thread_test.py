import multiprocessing


def worker(num):
    """thread worker function"""
    i = 0
    while True:
        i += 1
    print 'Worker:', num
    return


if __name__ == '__main__':
    jobs = []
    for i in range(3):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

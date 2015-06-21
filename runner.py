import json
from subprocess import Popen

def wait(workers):
    exit_process = True
    while exit_process:
         exit_process = pipe(workers,
            filter(_.poll() != None),
         )
    return  pipe(workers,
        filter(_.poll() == None),
     )

if __name__ == '__main__':
    worker_count = 10
    data = json.load(open("result.json"))

    workers = []

    for i, d in enumerate(data):
        if len(workers) >= worker_count:
            wait(workers)
        print "run {}".format(d["product_asin"])
        print "{}/{}".format(i + 1, len(data))
        workers.append(Popen(["python", "main.py", d["product_asin"]]))


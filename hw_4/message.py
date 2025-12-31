import multiprocessing
import time
import codecs
from datetime import datetime
from threading import Thread


def process_a(queue_in: multiprocessing.Queue,
              queue_out: multiprocessing.Queue,
              delay_sec: int = 5) -> None:
    while True:
        msg = queue_in.get()
        if msg is None:
            queue_out.put(None)
            break

        time.sleep(delay_sec)
        queue_out.put(msg.lower())


def process_b(queue_in: multiprocessing.Queue,
              queue_out: multiprocessing.Queue) -> None:
    while True:
        msg = queue_in.get()
        if msg is None:
            queue_out.put(None)
            break

        encoded = codecs.encode(msg, "rot_13")
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {encoded}", flush=True)
        queue_out.put((timestamp, encoded))


def drain_b_out(queue_b_out: multiprocessing.Queue) -> None:
    while True:
        item = queue_b_out.get()
        if item is None:
            break


def main() -> None:
    queue_a_in = multiprocessing.Queue()
    queue_a_to_b = multiprocessing.Queue()
    queue_b_out = multiprocessing.Queue()

    proc_a = multiprocessing.Process(target=process_a, args=(queue_a_in, queue_a_to_b))
    proc_b = multiprocessing.Process(target=process_b, args=(queue_a_to_b, queue_b_out))

    proc_a.start()
    proc_b.start()

    consumer_thread = Thread(target=drain_b_out, args=(queue_b_out,), daemon=True)
    consumer_thread.start()

    try:
        while True:
            try:
                msg = input()
            except EOFError:
                break

            if not msg:
                break

            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] (you) {msg}", flush=True)

            queue_a_in.put(msg)

    except KeyboardInterrupt:
        pass
    finally:
        queue_a_in.put(None)

        proc_a.join()
        proc_b.join()

        consumer_thread.join(timeout=2)

        queue_a_in.close()
        queue_a_to_b.close()
        queue_b_out.close()


if __name__ == "__main__":
    main()
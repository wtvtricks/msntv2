import serve
import os
import thread
import time


if __name__ == '__main__':
    if not os.path.exists(serve.home_directory):
        os.makedirs(serve.home_directory)

    if not os.path.exists(serve.images_shared_directory):
        os.makedirs(serve.images_shared_directory)
    time.sleep(3)
    thread.run()

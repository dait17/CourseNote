import os
from Views import Generated

if __name__ == '__main__':
    g = Generated()
    g.generate()

    os.system('python main.py')




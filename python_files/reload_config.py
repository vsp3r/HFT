FIFO_PATH = 'mypipe'

def reload_bot_config():
    with open(FIFO_PATH, 'w') as fifo:
        fifo.write('reload')

if __name__ == '__main__':
    reload_bot_config()

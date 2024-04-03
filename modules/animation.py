import time
import os
try:
    import pressure
except ModuleNotFoundError:
    from modules import pressure, steppers

# ASCII Art frames
frames = [
    '''
    _________
   |         |
   |         |
   |    O--o |
   |         |
   |_________|
  MOTORS RUNNING
''',
'''
    _________
   |         |
   |         |
   |    O    |
   |     \   |
   |______o__|
  MOTORS RUNNING.
''',
    '''
    _________
   |         |
   |         |
   |    O    |
   |    |    |
   |____o____|
  MOTORS RUNNING..
''',
'''
    _________
   |         |
   |         |
   |    O    |
   |   /     |
   |__o______|
  MOTORS RUNNING...
''',
'''
    _________
   |         |
   |         |
   | o--O    |
   |         |
   |_________|
  MOTORS RUNNING
''',
'''
    _________
   |  o      |
   |   \     |
   |    O    |
   |         |
   |_________|
  MOTORS RUNNING.
''',
'''
    _________
   |    o    |
   |    |    |
   |    O    |
   |         |
   |_________|
  MOTORS RUNNING..
''',
'''
    _________
   |      o  |
   |     /   |
   |    O    |
   |         |
   |_________|
  MOTORS RUNNING...
'''
]

def play(repeat=10, delay=0.2):
    quick_end = False
    for _ in range(repeat):
        if quick_end: break
        for frame in frames:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
            in_bin=(pressure.getValue() > 10)
            print(frame + f"Lid Opening\n" + f"Package in bin: {in_bin}")
            time.sleep(delay)
            if (in_bin):
                quick_end = True
                time.sleep(1)
                break

    for _ in range(3):
        for frame in reversed(frames):
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
            print(frame + f"Lid Closing\n" + f"Package in bin: {in_bin}")
            time.sleep(delay)

if __name__=="__main__":
    play()
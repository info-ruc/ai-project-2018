import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
import win32gui, win32ui, win32con, win32api
import pyautogui


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D] boolean values.
    '''
    output = [0,0,0]
    
    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1
    return output

    
file_name = 'training_data1.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []

def main():

    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    last_time = time.time() 
    while(True):
        # 800x600 windowed mode
        screen = grab_screen(region=(0,40,1600,940))
        
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # resize to something a bit more acceptable for a CNN
        screen = cv2.resize(screen, (160,90))
        keys = key_check()
        output = keys_to_output(keys)
        training_data.append([screen,output])
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        if len(training_data) % 100 == 0:
            print(len(training_data))
            np.save(file_name,training_data)
            if(len(training_data) == 14000):
                nexttime = time.time()
                print(nexttime - last_time)
                print("It's OK!!!!!")
                break
if __name__ == "__main__":

    main()
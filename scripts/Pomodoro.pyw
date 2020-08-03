# !/usr/bin/env python3
#"""
#    This script changes the C:\Windows\System32\drivers\etc\hosts file to block any
#    website during a certain period of time.

#    Process:
#    1. Open hosts file to read and write
#    2. Modify file to add blocked sites IF within timer. Close file
#    3. When timer finished, Open file again modify file and delete blocked websites
#"""

import time
import datetime as dt

import tkinter
from tkinter import messagebox
from tkinter import simpledialog
import winsound
from threading import Thread

class Pomodoro(Thread):
    # using the r'' string format gives the raw data, to prevent "escapes" of any backlash
    # Trial path for development
    hosts_path = r'C:\Windows\System32\drivers\etc'
    redirect_path = "127.0.0.1"
    # check paths are read correctly by pc
    print("-"*40+f"\nCurrent host path: \n{hosts_path}"+"\n"+"-"*40)

    website_list = ["www.facebook.com","facebook.com","imgur.com","www.imgur.com"]

    def __init__(self):
        Thread.__init__(self)
        self.t_now = dt.datetime.now()
        self.timenow = self.t_now.strftime("%H:%M")

    # Run main loop, to block all sites while is running
    def add_websites(self, filepath):
        with open(filepath+"/hosts","r+") as dummy_file:
            content = dummy_file.read()
            # Now, we need to check if the websites are already in the content. If they are
            # don't do anything. If they are not, go add them
            for website in self.website_list:
                if website in content:
                    #print('Websites blocked successfully!')
                    pass
                else:
                    dummy_file.write(self.redirect_path+"\t"+website+"\n")
                    #print('Website blocked -> added')

    def remove_websites(self, filepath):
        with open(filepath+"/hosts","r+") as file:
            content = file.readlines()          # content is now a list with strings for each line in the text file
            file.seek(0)
            # iterate through lines of conent.
            for lines in content:
                # If the website string is not in the line, boolean will be True, therefore, write that line again
                if not any(website in lines for website in self.website_list):
                    file.write(lines)
                    # print('written')
            # truncating a file deletes everything forward from the point it ended at
            file.truncate()

    def run(self):
        total_pomodoros = 0
        

        ## Main script here:
        # Collect time information
        t_now = dt.datetime.now()                       # Current time for reference.   [datetime object]
        t_pom = 25*60                                   # Pomodoro time                 [int, seconds]
        t_delta = dt.timedelta(0,t_pom)                 # Time delta in mins            [datetime object]
        t_fut = t_now + t_delta                         # Future time for reference     [datetime object]
        delta_sec = 1#60                                  # Break time, after pomodoro    [int, seconds]
        t_fin = t_now + dt.timedelta(0,t_pom+delta_sec) # Final time (w/ 5 mins break)  [datetime object]
        print(f"Bug check 0: \nt_now: {t_now}\nt_fut: {t_fut}")

        # GUI set pomodoro in motion!
        messagebox.showinfo("Pomodoro Started!", "\nIt is now "+t_now.strftime("%H:%M") +
        " hrs. \nTimer set for 25 mins.")

        # Main script
        while True:
            # Pomodoro time! Code for adding and maintaining the websites to be blocked!
            if t_now < t_fut:
                self.add_websites(self.hosts_path)
                print('First tnow < tfut')
            ## Commented out. Uncomment to add a break of 5 mins into the comodoro!
            ## it is now past working pomodoro, within the break. Delete the websites
            elif t_fut <= t_now <= t_fin:
                # allow for browsing again. Remove websites from hosts file
                print('Break time!')
                self.remove_websites(self.hosts_path)
            #Pomodoro and break finished. Check if ready for another pomodoro!
            else:
                print('Third tnow > tfut - Finished')
                # Ring a bell (with print('\a') to alert of end of program.
                print('\a')
                # Annoy!
                for i in range(10):
                    winsound.Beep((i+100), 500)
                self.remove_websites(self.hosts_path)
                usr_ans = messagebox.askyesno("Pomodoro Finished!","Would you like to start another pomodoro?")
                #usr_ans = input("Timer has finished. \nWould you like to start another pomodoro? \nY/N:  ")
                total_pomodoros += 1
                if usr_ans == True:
                    # user wants another pomodoro! Update values to indicate new timeset.
                    t_now = dt.datetime.now()
                    t_fut = t_now + dt.timedelta(0,t_pom)
                    t_fin = t_now + dt.timedelta(0,t_pom+delta_sec)
                    continue
                elif usr_ans == False:
                    print(f'Pomodoro timer complete! \nYou have completed {total_pomodoros} pomodoros today.')
                    # unlock the websites
                    # Show a final message)
                    messagebox.showinfo("Pomodoro Finished!", "\nIt is now "+self.timenow+
                    "\nYou completed "+str(total_pomodoros)+" pomodoros today!")
                    break
            # check every 3 seconds and update current time
            time.sleep(20)
            t_now = dt.datetime.now()
            self.timenow = t_now.strftime("%H:%M")
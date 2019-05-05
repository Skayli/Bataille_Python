from tkinter import *
import time
import threading
from random import random
import queue as Queue
from vue.cadre import *

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        # self.gui = gui

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = Cadre(self.queue)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        # self.thread1 = threading.Thread(target=self.workerThread1)
        # self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.gui.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(random() * 0.3)
            msg = "message"
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

    def getGUI(self):
        return self.gui

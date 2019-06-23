from machine import Pin
import time
from config import config
from XRotorESCDriver import XRotorESCDriver
from PA_ESC_Component import PA_ESC_Component
from PyAutopilot import PyAutopilot


def main():
    py_autopilot = PyAutopilot()
    py_autopilot.run()
    pass


main()

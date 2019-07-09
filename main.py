from pachewie import PAChewie
import timer


def main():
    timer.init_timers()
    pa_chewie = PAChewie()
    pa_chewie.run()
    # _thread.start_new_thread(loop, ())
    # time = Timer(0)
    # time.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: machine.reset())


main()

# PyAChewie

PyAutopilotChewie is flying control system based on micropython


Project structure:
- /mian.py: Entry point (init PyAchewie class)
- /config.py: Configuration of Modules and Drivers (like. PIN, BAUDRATE of UART...)
- /driver_config.py: Configuration of that which drivers will be imported and used.
- /PAChewie.py: Main class, load modules and callback loop.
- /lib: include library, module, driver...
- /lib/PAC_Module_*: Module, like a subsystem.(Safe, Sensor, Control, CMD)
- /lib/PAC_LIB_*: Library
- /lib/PAC_DriverInterface_*: Interface between driver and module.
    - if you hardware(Sensor, ESC) is different from mine, you can implement these interfaces to write your driver.
- /lib/PAC_Driver_*: Driver between hardware and soft.


1. The `/lib(library)` directory maybe is not elegant.
> Reason : Workaround: Don’t install modules belonging to the same namespace package in different directories. For MicroPython, it’s recommended to have at most 3-component module search paths: for your current application, per-user (writable), system-wide (non-writable). 
>> refer from : http://docs.micropython.org/en/latest/genrst/core_language.html#micropython-does-t-support-namespace-packages-split-across-filesystem

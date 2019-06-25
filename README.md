## PyAChewie project
[PyAutopilotChewie](https://github.com/HotIce0/PAChewie) is flying control system based on [micropython](https://github.com/micropython/micropython).

This project was inspired by a scene from a Hollywood movie I have seen, but unfortunately I forgot the name of the movie. I am a software developer like me, I am always interested in the quadcopter, but my foundation is not good, the hardware Has only learned C51, just right, I need to complete my undergraduate graduation design in 2020. First feeling, yes, this is what I want. My goal is to develop a  flight control system based on micropython with a clear project structure that is easier to learn For people who want to write their own flight control system. Then, build some artificial intelligence application on this system to implement interesting features.


### Project structure:
- /mian.py: Entry point (init PAChewie class)
- /config.py: Configuration of Modules and Drivers (like. PIN, BAUDRATE of UART...)
- /driver_config.py: Configuration of that which drivers will be imported and used.
- /pachewie.py: Main class, load modules and callback loop.
- /lib: include library, module, driver...
- /lib/module_*: Module, like a subsystem.(Safe, Sensor, Control, CMD)
- /lib/lib_*: Library
- /lib/driver_interface_*: Interface between driver and module.
    - if you hardware(Sensor, ESC) is different from mine, you can implement these interfaces to write your driver.
- /lib/driver_*: Driver between hardware and soft.


1. The `/lib(library)` directory maybe is not elegant.
> Reason : Workaround: Don’t install modules belonging to the same namespace package in different directories. For MicroPython, it’s recommended to have at most 3-component module search paths: for your current application, per-user (writable), system-wide (non-writable). 
>> refer from : http://docs.micropython.org/en/latest/genrst/core_language.html#micropython-does-t-support-namespace-packages-split-across-filesystem

### Contributing
PyAChewie is an open-source project and welcomes contributions. To be productive, please be sure to follow the [Code Conventions](https://github.com/HotIce0/PAChewie/blob/master/CODECONVENTIONS.md). Note that **PyAChewie** is licenced under the **GNU General Public License V3.0**, and all contributions should follow this license.
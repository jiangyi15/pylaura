Laura++ Interface for Python
==============================

This project is based on [Laura++](https://laura.hepforge.org/) and [cffi](https://github.com/python-cffi/cffi), in order to provide python module for Laura++.

Requirement
-----------

Since Laura++ required [ROOT](https://root.cern.ch), you should install ROOT first.
And then you should build and install Laura++. The C/C++ compiler is required.

Installation
------------



You can download it and build from source.
```
git clone https://github.com/jiangyi15/pylaura.git
cd pylaura
pip install .
```

Or you can directly for github
```
pip install git+https://github.com/jiangyi15/pylaura.git
```

If your Laura++ installation is not in the standard location.
You can use `CFLAGS`, `CXXFLAGS` and `LDFLAGS` enviroment variable to install.
For example, if you build Laura++ in the `../build` location, you can use the following command
```
CFLAG=-I`pwd`/../build/inc CXXFLAG=-I`pwd`/../build/inc LDFLAG=-L`pwd`/../build/lib   pip install .
```

Examples
--------

```
from laura import LauraModel

model = LauraModel("B0", "pi+", "pi-", "D0_bar")
model.init_from_jsonfile("model.json", "model_item")
print(model(11., 9)) # m13Sq, m23Sq
```
if would return the amplitude (getDynamicAmp) of all resonances.


Note
----

If there is the following error
```
ImportError: libLaura++.so.3: cannot open shared object file: No such file or directory
```

You can use `LD_LIBRARY_PATH` enviroment variable to start `python`.
```
LD_LIBRARY_PATH=`pwd`/../build/lib` python
```

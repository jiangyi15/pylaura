from cffi import FFI
import os


ffibuilder = FFI()

dir_path = os.path.dirname(__file__)
ap = lambda x: os.path.join(dir_path, x)

with open(ap("laura.h")) as f:
    source = f.read()

ffibuilder.cdef(source)

include_dirs=[dir_path]
if "LAURA_INCLUDE_DIR" in os.environ:
    include_dirs.append(os.environ["LAURA_INCLUDE_DIR"])

library_dirs=[]
if "LAURA_LIBRARY_DIR" in os.environ:
    library_dirs.append(os.environ["LAURA_LIBRARY_DIR"])

extra_compile_args = []
if "CFLAGS" in os.environ:
    extra_compile_args.append(os.environ["CFLAGS"])

extra_link_args = []
if "LDFLAGS" in os.environ:
    extra_link_args.append(os.environ["LDFLAGS"])


ffibuilder.set_source("_laura_lib",
                      '#include "laura.h"',
                      sources=[ap("laura.cpp")],
                      include_dirs=include_dirs,
                      library_dirs=library_dirs,
                      libraries=["Laura++"],
                      extra_compile_args = extra_compile_args,
                      extra_link_args=extra_link_args)

if __name__=="__main__":
    ffibuilder.compile(verbose=True)


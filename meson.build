project('pylaura', 'c', 'cpp')

py = import('python').find_installation(pure: false)

install_subdir(
    'laura',
    install_dir: py.get_install_dir(),
)

ext_src = custom_target(
    command: [py, files('laura_build.py')],
    output: ['_laura_lib.c']
)

luara_lib = declare_dependency(
  compile_args: [],
  link_args: ['-lLaura++']
)

py.extension_module(
    '_laura_lib',
    ext_src ,
    'laura.cpp',
    install: true,
    dependencies: [py.dependency(), luara_lib],
    limited_api: '3.8',
)

#
# py.extension_module(
#     '_looptools_lib',
#     ['_looptools_lib.c'],
#     include_directories : ['LoopTools-2.16/build'],
#     install: true,
# )

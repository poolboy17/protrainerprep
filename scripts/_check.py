import py_compile, sys
try:
    py_compile.compile(r'D:\dev\projects\protrainerprep\protrainer-pipe.py', doraise=True)
    print('OK — compiles clean')
except py_compile.PyCompileError as e:
    print(f'FAIL: {e}')
    sys.exit(1)

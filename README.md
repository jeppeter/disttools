# cmdpack
> python package for release debug to release source code

### Release History
* Mar 20th 2017 Release 0.1.0 to release first version


### simple example
```python

```

> if the command line like this
> python script.py
 
> result is like this
```shell
hello
ok
```

> this package ,just to make the cmdpack as filter out

## run out
```python
import cmdpack
import sys


def test_outline():
    cmds = []
    cmds.append('%s'%(sys.executable))
    cmds.append(__file__)
    cmds.append('cmdout')
    cmds.append('hello')
    cmds.append('world')
    for l in cmdpack.run_cmd_output(cmds):
        print('%s'%(l))
    return

def cmdoutput(args):
    for c in args:
        print('%s'%(c))
    sys.exit(0)
    return

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == 'cmdout':
        cmdoutput(sys.argv[2:])
        return
    test_outline()
    return

if __name__ == '__main__':
    main()
```

> shell output
```shell
hello
world
```


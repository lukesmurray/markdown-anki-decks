# Python

## Which python 3 module contains classes for representing file system paths?

[`pathlib`](https://docs.python.org/3/library/pathlib.html)

## In python how do force an exception to occur?

```python
raise Exception("exception message")
```

## In python 3 how do you handle an exception and print the exception message?

You use the syntax `try ... except`.  
You can specify the type of exception which is captured using `except <Exception Type>`.  
You can access the exception for further handling using `except Exception as e`.

```python
try:
  raise Exception("exception message")
except Exception as e:
  print(e)
```

> Handling run-time error: division by zero

## In python 3 how do you make a pathlib path absolute?

Call `Path.resolve` which creates a new path object which is absolute with all symlinks resolved.

```python
p = Path()
print(p)
p = p.resolve()
print(p)
```

> '.'  
> '/home/antoine/pathlib'

## How do you install or upgrade a package using pip?

```sh
pip install [package_name] --upgrade
```

or

```sh
pip install [package_name] -U
```

# Python

- ref
	[https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-11-on-ubuntu-20-04-and-22-04-lts/](https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-11-on-ubuntu-20-04-and-22-04-lts/)
	
	[https://docs.python.org/3/library/inspect.html#module-inspect](https://docs.python.org/3/library/inspect.html#module-inspect)
	
	[https://docs.python.org/3/glossary.html](https://docs.python.org/3/glossary.html)
	
	[https://web.stanford.edu/class/physics91si/2013/handouts/Pdb_Commands.pdf](https://web.stanford.edu/class/physics91si/2013/handouts/Pdb_Commands.pdf)
	

```bash
python3 -m pdb <"python file to debug">;
```

- dashes are illegal in Python identifiers
- The `sys.path` list contains all the directories that Python will search for modules when you try to import them.

## Python version mapping (multiple python version)

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update

apt list | grep python3.11

sudo apt-get install python3.11

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2

sudo update-alternatives --config python3

python3 -V
```

### Create wheel setup for python

```python

```

# GIL

- ref
    
    [https://en.wikipedia.org/wiki/Global_interpreter_lock](https://en.wikipedia.org/wiki/Global_interpreter_lock)
    

**Global interpreter lock** : A global interpreter lock is a mechanism used in computer-language interpreters to synchronize the execution of threads so that only one native thread (pre process) can execute one thread to execute at a time, even if run on a multi-core processor.

- application running on implementations with a GIL can be designed to use separate processes to achieve full parallelism, as each process has its own interpreter and in turn has its own GIL.
- otherwise the GIL can be a significant barrier to parallelism.

# Serialize or De-serialize

# Supervisor

- ref
    
    [http://supervisord.org/](http://supervisord.org/)
    
    [https://docs.python.org/3/library/configparser.html](https://docs.python.org/3/library/configparser.html)
    

```bash
pip install supervisor
```

## json

- The `Person` class has attributes `name` and `age`.
- The `convert_to_dict` function is defined to convert a `Person` object into a dictionary, which is JSON serializable.
- The `default=convert_to_dict` argument is passed to `json.dumps()`, telling it to use `convert_to_dict` for any non-serializable objects encountered.

```python
import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def convert_to_dict(obj):
    if isinstance(obj, Person):
        return obj.__dict__
    raise TypeError("Type not serializable")

person = Person(name="John", age=30)
json_string = json.dumps(person, default=convert_to_dict)

print(json_string)
```

# Data Validation

`pydentic` : python widely used data validation library.

## encoding decoding

```python
import hashlib, base64
original_bytes = bytes.fromhex(hex_value); # get hex value form hex decoded.
```

## Setup tool

```python
# setup.py

from setuptools import setup, find_packages

setup(
    name='your_package',
    version='0.1.0',
    author='Your Name',
    description='Description of your package',
    packages=find_packages(),
    install_requires=[],  # List any dependencies your package requires
)
```

```bash
# run from root directory
python setup.py sdist bdist_wheel
```

### Window setup activate-env

- ref
    
    https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3
    

```bash
# setup for activate.bat to take effect in poweshell
Get-ExecutionPolicy -List
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip `setup.py` file setup

```jsx
from setuptools import setup, find_packages

setup(
    name='package_name',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'dependency1',
        'dependency2',
        # Add any additional dependencies here
    ],
    entry_points={
        'console_scripts': [
            'package_name=package_name.__main__:main'
        ]
    }
)
```

yaml file - is a data serialization language.

abstract meaning - existing in thought or as an idea but not having a physical or concrete existence.

- separately form something else.
- a summary

instance meaning - occurrence of something.

pip - preferred installer program.

dn - distinguished name.

descriptor - python descriptors are a way to create managed attributes.

- protect an attribute from changes or to automatically update the values of a dependent attribute.
- descriptors let objects customize attribute lookup, storage, and deletion.

offset - an offset within an array or other data structure object is an integer indicating the distance (displacement) between the beginning of the object and a given element or point, within the same object.

POC meaning - Proof Of Concept, An advanced demo project that reflects a real- word scenario.

derived class - a class that is constructed from a base class or an existing class.

sentinel - are the singleton objects that typically represent some terminating (end) condition or have a special, symbolic meaning. (like python build in `None`)

file descriptor or file handlers - number (non negative integer) that uniquely identifies an open file in a computer’s operating system.

- it describes a data resource, and how that resource may be accessed.
- when a process makes a successful request to open a file, the kernel returns a file descriptor which points to an entry in the kernel’s global file table.

### Managing pip constraint files and packages

```bash
pip install "apache-airflow[crypto,celery,postgres,kubernetes,docker]"==1.10.12 --constraint ./requirements-python3.8.txt
pip install <package name> --no-cache-dir; # do not use cache files.
pip-autoremove <package name> -y; # remoe all the dependencies also.
deactivate & exit; # to exit from the venv shell.
pipenv install -r <requirement.file path>
pipenv install; # init env for the current path.
pipenv shell; # initiate the virtual env.
pip freeze > requirements.txt; # create current env pip packages list.
```

bound methods - if a function is an attribute of class and it is accessed via the instances, they are called bound methods.

- the methods with the `self` argument at the beginning are the bounds methods. These are dependent on the instance of the classes, known as instance methods.

unbound methods - 

- cannot call this methods using a class instance. *Static methods* are example of unbound method.

static methods - 

- deals with the arguments it takes.

### XML parsing

- reference
    
    [https://lxml.de/parsing.html](https://lxml.de/parsing.html)
    

```python
from lxml import etree

# parsers
root = etree.fromstring("""xml file here""")
etree.tostring() # return in formaat b'' string;
etree.parse()
etree.XMLParser()
```

# Processes

## Sub process

```python
result = subprocess.run(['path/to/your/binary/executable'], stdout=subprocess.PIPE, text=True)
```

## Thread process

- reference
    
    [https://docs.python.org/3/library/threading.html](https://docs.python.org/3/library/threading.html)
    

### See the threads currently running

use `threading.enumerate()` function, this returns a list of all the Thread objects that are currently active in the program.

```python
import threading

# Print the names of all of the active threads
for thread in threading.enumerate():
    print(thread.name)
```

using `active_count()` function to get the number of active threads in the program, return the total number of active threads in the program.

### Terminating the thread process

1. Using the `thread.exit()`. Called from within the thread to terminate the thread. It Does not allow the thread to clean up after itself or release any resources it may be holding.
2. Using a flag variable. Use a flag variable that the thread checks periodically when the flag variable that the thread checks periodically.
    1. `threading.Event().is_set()`   
    2. `thread.join()` method is called on a thread, the calling thread will block until the target thread has finished executing. This can be used to terminate a thread by calling `join()` on the thread from the main thread or another thread.
        1. allows to wait for a thread to complete its execution.
        2. support the use of `TIMEOUT_MAX` . Takes an optional argument `timeout` argument.
        3. the error `cannot join current thread` can occur when `join()` method call on the thread that is currently running, because current thread cannot be joined to itself.
        4. the error `cannot wait on un-acquired lock` can occur when using the `threading.Condition()` . If you try to call the `wait()` method without first acquiring the lock associated with the condition. 
        5. The Condition class provides a way to synchronize the execution of threads by allowing them to wait for a certain condition to be met before continuing.
            1. to use condition. Create a `Lock` object and acquire it, and then call the `wait()` method on the `Condition` , the `wait()` method releases the lock and blocks the current thread until the condition is set or the optional timeout is reached.
            2. If the calling thread has not acquired the lock when this method is called, a `RuntimeError` is raised.
    3.  `threading.Thread.stop()` method not recommended to use this method (deprecation), it can leave resources in an undefined state and can cause problems with the interpreter.

# Errors

- The `urllib3.exceptions.ProtocolError` typically occurs when there is an issue with the protocol being used during an HTTP request. This error is part of the `urllib3` library, which is commonly used for making HTTP requests in Python.
1. **Incorrect URL Format:** Ensure that the URL you are trying to access is correctly formatted. It should include the protocol (e.g., `http://` or `https://`) and the correct domain.
2. **SSL/TLS Issues:** If you are using HTTPS (SSL/TLS) and there are certificate issues or the server is misconfigured, you might encounter a protocol error.
3. **Server-Side Issues:** The server might not be responding according to the HTTP protocol. Check the server logs for any issues.

# sorting

```python
# Sort the list of dictionaries based on multiple keys: first 'age', then 'name'
sorted_j_list = sorted(j_list, key=lambda x: (x['age'], x['name']))
```

## Deleting variables and garbage collection

```python
import gc

# Create a variable
my_variable = 42

# Delete the variable and force garbage collection
del my_variable
gc.collect()
```

# Use of type function to create type of class

```python
# Define the custom exception class
class MyException(Exception):
    def __init__(self, message="This is a custom exception"):
        self.message = message
        super().__init__(self.message)

# Use the type function to create a new type for the custom exception
MyExceptionType = type("MyExceptionType", (MyException,), {})

# Raise an instance of the custom exception
raise MyExceptionType("Custom exception message")|
```

# CSV file reading and writing

Comma separated values - most common import and export format for spreadsheets and databases.

- describe the format in a standardized way in RFC 4180
- read write sequences. programmers can also read and write data in dictionary form using the `DictReader` and `DictWriter` classes.
- implements classes to read and write tabular data in CSV format. preferred by Excel and generated by Excel.

delimiter meaning - a blank space, comma or other character or symbol that indicates the beginning or end of a character string, word or data item.

- sequence of one or ore characters for specifying the boundary between separate, independent regions in plain text.

## modules

csvfile - can be any object which supports the iterator protocol and returns a string each time its `__next__()` method is called.

- if csvfile is a file object, it should be opened with `newline=''`

```python
import csv

with open('eggs.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))
```

reader 

- return a reader object which will over lines in the given csvfile.

# Pages

[Logging](https://www.notion.so/Logging-67f221caa6f64034bab233fbe9ecfe95?pvs=21)

[Modules](https://www.notion.so/Modules-439cb6e548a84189bf35a41b7ddc5369?pvs=21)

[Exceptions](https://www.notion.so/Exceptions-39a4316f57e24081bbd0e023c1b4312f?pvs=21)

[Cryptography](https://www.notion.so/Cryptography-1df6d46242a34c25b3e6ee78bf83a202?pvs=21)

---

[Imports System](https://www.notion.so/Imports-System-d960ccaaf53f4d5d88b0503772aebb94?pvs=21)

[CLI](https://www.notion.so/CLI-ae01cb22e6e2483ba6e4134a402c4dc5?pvs=21)

[topics](https://www.notion.so/topics-35ad2f8d9c054745bd718a5c58e46e17?pvs=21)
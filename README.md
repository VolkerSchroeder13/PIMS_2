# PIMS
## Setup
### Python

First of all you need to make sure that Python is installed.

Check if python is installed by typing the following line in shell / command-prompt:

    python -V
    
or eventually:

    python3 -V
    
You should get a similar output like this:

    Python 3.10.2
    
If you don't get an output like this or an error message, you should install Python first.

You can get it [here](https://www.python.org/downloads/).

Or if you using Linux, you can simply paste following commands in your shell:

    $ sudo apt-get update
    $ sudo apt-get install python3.10

In development i'm using the following version:

    Python 3.10.2
  
To make sure everything is working fine, you should have at least the version mentioned above.

### PIP

To install python packages I'm using pip with the following version:

    pip 21.2.4 from C:\Python310\lib\site-packages\pip (python 3.10)
    
To make sure everything is working fine, you should have at least the version mentioned above.

Note: PIP can be automatically installed with python together.

### Virtual environment

I am using a virtual environment (short venv) to prevent e.g. package name duplications.

To set up a venv, you need to have virtualenv installed.

You can install it by typing the following line in your prompt:

    pip install virtualenv
    
I am using the following version of virtualenv:

    virtualenv==20.13.0
    
You can check your version of virtualenv by using following command:

    pip show virtualenv

The output should look like this:

    Name: virtualenv
    Version: 20.13.0
    Summary: Virtual Python Environment builder
    Home-page: https://virtualenv.pypa.io/
    Author: Bernat Gabor
    Author-email: gaborjbernat@gmail.com
    License: MIT
    Location: c:\python310\lib\site-packages
    Requires: six, filelock, platformdirs, distlib
    Required-by: pipenv

Now, in your project directory you can create a virtual environment by typing the following line:

    python -m venv [NAME OF VENV]
    
Note: Replace [NAME OF VENV] with a name you like. I'm usually using "venv" as the name of the virtual environment for simplicity.

You can activate the virtual environment as following:

On windows:

    \venv\Scripts\activate
    
On Linux:

    source \venv\bin\activate.sh
    
Now you're ready to install required packages in the environment by hitting the following line:

    pip install -r requirements.txt
    
Note: You need to be in the same directory where requirements.txt is located.


## How to run

### Scrapy

TODO: Update this, when actual program is existing

Right now, you can only start single spiders to crawl specific websites.
(You can see them in the spiders directory).
Execute following command in PIMS/ directory:

    scrapy crawl [NAME OF SPIDER]

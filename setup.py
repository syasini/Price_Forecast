from setuptools import setup, find_packages

# read the contents of requirements.txt
with open("requirements.txt", "r") as f:
    reqs = [line.rstrip("\n") for line in f if line != "\n"]

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='gold_silver_price',
      version='0.0.0',
      description='a library for forecasting the price of gold and silver!',
      url='https://github.com/syasini/Gold_Silver_Forecast',
      install_requires=reqs,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Siavash Yasini',
      author_email='siavash.yasini@gmail.com',
      packages=find_packages(),
      )

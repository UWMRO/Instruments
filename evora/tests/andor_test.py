import unittest
import sys
  
# setting path
sys.path.append('../evora')
from andor import *


def test_initialize():
   assert initialize() == 20002


def main():
   test_initialize()


if __name__ == '__main__':
   main()

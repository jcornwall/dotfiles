import os
import logging

def IsHeaderFile(filename):  
  ext = os.path.splitext(filename)[1]
  return ext in [".h", ".hpp"]

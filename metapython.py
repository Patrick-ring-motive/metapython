def xargs(*args, **kwargs):
  return {'args': args, 'kwargs': kwargs}


def xapply(func, xargs):
  return func(*xargs['args'], **xargs['kwargs'])


import inspect
import re
import os
import sys
import logging
from subprocess import PIPE, run

hasIPy = False
try:
  from IPython import get_ipython
  hasIPy = True
except:
  hasIPy = False


def sh(command):
  try:
    result = run(command,
                 stdout=PIPE,
                 stderr=PIPE,
                 universal_newlines=True,
                 shell=True)
    if len(result.stdout) > 0:
      return result.stdout
    if len(result.stderr) > 0:
      return result.stderr
    return f"{result}"
  except Exception as e:
    return f"{e}"


logging.basicConfig(level=logging.INFO)


def importLib(lib):
  if re.search(r"[^a-zA-Z0-9_\.]", lib):
    logging.error("Invalid characters in library name.")
    return None
  try:
    module = __import__(lib)
    print(module)
    globals()[lib] = module
    try:
      inspect.currentframe().f_back.f_globals.update({lib: module})
    except:
      pass
    if hasIPy:
      get_ipython().user_global_ns[lib] = globals()[lib]
    logging.info(f"Successfully imported {lib}.")
    return module
  except Exception as e:
    logging.warning(f"{lib} not found, {e} attempting to install.")
    try:
      c = sh(f"conda install --yes {lib}")
      if "not found" in c:
        sh(f"pip install {lib}")
      module = __import__(lib)
      globals()[lib] = module
      try:
        inspect.currentframe().f_back.f_globals.update({lib: module})
      except:
        pass
      if hasIPy:
        get_ipython().user_global_ns[lib] = globals()[lib]
      logging.info(f"Successfully installed and imported {lib}.")
      return module
    except Exception as e:
      logging.error(f"Failed to install {lib}: {e}")
      return None


def importLibAs(lib, alias):
  if re.search(r"[^a-zA-Z0-9_\.]", lib):
    logging.error("Invalid characters in library name.")
    return None
  if re.search(r"[^a-zA-Z0-9_\]", alias):
    logging.error("Invalid characters in library alias.")
    return None
  try:
    module = __import__(lib)
    globals()[alias] = module
    try:
      inspect.currentframe().f_back.f_globals.update({alias: module})
    except:
      pass
    if hasIPy:
      get_ipython().user_global_ns[alias] = globals()[module]
    logging.info(f"Successfully imported {lib}.")
    return module
  except Exception as e:
    logging.warning(f"{lib} not found, {e} attempting to install.")
    try:
      c = sh(f"conda install --yes {lib}")
      if "not found" in c:
        sh(f"pip install {lib}")
      module = __import__(lib)
      globals()[alias] = module
      try:
        inspect.currentframe().f_back.f_globals.update({alias: module})
      except:
        pass
      if hasIPy:
        get_ipython().user_global_ns[alias] = globals()[module]
      logging.info(f"Successfully installed and imported {lib}.")
      return module
    except Exception as e:
      logging.error(f"Failed to install {lib}: {e}")
      return None


def importModule(lib, pkg):
  print(f"from {lib} import {pkg}")
  if re.search(r"[^a-zA-Z0-9_\.]", lib):
    print("Invalid characters in library name.")
    return None
  if re.search(r"[^a-zA-Z0-9_\.]", pkg):
    print("Invalid characters in module name.")
    return None
  try:
    globals()[lib] = __import__(lib, globals(), locals(), [pkg], 0)
    globals()[pkg] = getattr(globals()[lib], pkg)
    try:
      inspect.currentframe().f_back.f_globals.update({pkg: globals()[pkg]})
    except:
      pass
    if hasIPy:
      get_ipython().user_global_ns[pkg] = globals()[pkg]
    print(f"Successfully imported {lib}.")
    print(globals()[pkg])
    return globals()[pkg]
  except Exception as e:
    print(f"{lib} not found, {e} attempting to install.")
    try:
      c = sh(f"conda install --yes {lib}")
      if "not found" in c:
        print(sh(f"pip install {lib}"))
      globals()[lib] = __import__(lib, globals(), locals(), [pkg], 0)
      globals()[pkg] = getattr(globals()[lib], pkg)
      try:
        inspect.currentframe().f_back.f_globals.update({pkg: globals()[pkg]})
      except:
        pass
      if hasIPy:
        get_ipython().user_global_ns[pkg] = globals()[pkg]
      print(f"Successfully installed and imported {lib}.")
      return globals()[pkg]
    except Exception as e:
      print(f"Failed to install {lib}: {e}")
      return None


def importModuleAs(lib, pkg, alias):
  if re.search(r"[^a-zA-Z0-9_\.]", lib):
    logging.error("Invalid characters in library name.")
    return None
  if re.search(r"[^a-zA-Z0-9_\.]", pkg):
    logging.error("Invalid characters in module name.")
    return None
  if re.search(r"[^a-zA-Z0-9_\]", alias):
    logging.error("Invalid characters in module alias.")
    return None
  try:
    globals()[lib] = __import__(lib, globals(), locals(), [pkg], 0)
    globals()[alias] = getattr(globals()[lib], pkg)
    try:
      inspect.currentframe().f_back.f_globals.update({alias: globals()[pkg]})
    except:
      pass
    if hasIPy:
      get_ipython().user_global_ns[alias] = globals()[alias]
    logging.info(f"Successfully imported {lib}.")
    return globals()[alias]
  except Exception as e:
    logging.warning(f"{lib} not found, {e} attempting to install.")
    try:
      c = sh(f"conda install --yes {lib}")
      if "not found" in c:
        sh(f"pip install {lib}")
      globals()[lib] = __import__(lib, globals(), locals(), [pkg], 0)
      globals()[alias] = getattr(globals()[lib], pkg)
      try:
        inspect.currentframe().f_back.f_globals.update({alias: globals()[pkg]})
      except:
        pass
      logging.info(f"Successfully installed and imported {lib}.")
      return globals()[alias]
    except Exception as e:
      logging.error(f"Failed to install {lib}: {e}")
      return None
      
def magic(str):
  if hasIPy:
    get_ipython().magic(str)
  else:
    print(f"This is where a notebook would run magic {str}")

def fromImport(lib, pkgs):
  for pkg in pkgs:
    globals()[pkg] = importModule(lib, pkg)
  return globals()


def fromImportAs(lib, pkgs):
  for pkg in pkgs:
    importModuleAs(lib, pkg, pkgs[pkg])


def none():
  return None


def tryrun(function, fargs):
  try:
    return xapply(function, fargs)
  except:
    return None


def Q(function, fargs):
  return tryrun(function, fargs)


def getattry(obj, attribute):
  try:
    return inspect.getmembers(obj).__getattribute__(attribute)
  except:
    return None


def getitem(obj, item):
  try:
    return obj[item]
  except:
    return None


def getprop(obj, prop):
  try:
    if re.search("[^a-zA-Z0-9_]", prop) != None:
      return None
    return eval('obj.' + prop)
  except:
    return None


def getany(obj, any):
  try:
    return (getattry(obj, any) or getitem(obj, any) or getprop(obj, any))
  except:
    return None


def delitem(obj, item):
  try:
    del obj[item]
    return obj
  except:
    return obj


def delattry(obj, attr):
  try:
    delattr(obj, attr)
    return obj
  except:
    return obj


def delprop(obj, prop):
  try:
    if re.search("[^a-zA-Z0-9_]", prop) != None:
      return obj
    eval('del obj.' + prop)
    return obj
  except:
    return obj


def delany(obj, any):
  try:
    return (delattry(obj, any) or delitem(obj, any) or delprop(obj, any))
  except:
    return obj


def setattry(obj, attribute, value):
  try:
    setattr(obj, attribute, value)
    return True
  except:
    return False


def setitem(obj, item, value):
  try:
    obj[item] = value
    return True
  except:
    return False


def setprop(obj, prop, value):
  try:
    if re.search("[^a-zA-Z0-9_]", prop) != None:
      return False
    eval('obj.' + prop + ' = value')
    return True
  except:
    return False


def setany(obj, any, value):
  try:
    return (setattry(obj, any, value) or setitem(obj, any, value)
            or setprop(obj, any, value))
  except:
    return False

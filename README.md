# sections_dataset_generator WIP 

set of modules used with rhino+grasshopper dev

most of modules reqire usage of conda venv provided (py27)

## Modules sctructure 
  - gblock - main functional module, moslty obsolete 
    - gblock.elements - current set of core classes, moving from old structure, currently implementing 
    - gblock.gh_context - current version of gh dev context initialisation methods. Obsolete, moving to separate module -> ghdev  
  - ghdev - wip module, replacement for gblock.gh_context, no stable version yet 
  
## dependencies
  - anaconda\miniconda current version 
  - python=2.7.15
  - xarray=0.11.3
  - qtawesome=0.7
  - gh-remote-python
    https://www.food4rhino.com/en/app/gh-python-remote
    https://pypi.org/project/gh-python-remote/

## installation
  - create new conda venv (or import provided)
  ```
  conda create --name py27 -c conda-forge python=2.7 numpy pandas xarray qtawesome=0.7 rpyc
  conda activate py27
  pip install gh-python-remote
  python -m ghpythonremote._configure_ironpython_installation
  pip install Rhino-stubs 
  ```
  - clone this repo. Make sure .gh script files are in the same folder as modules 
 
  

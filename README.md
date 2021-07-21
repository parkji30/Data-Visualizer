# Treemap Visualizer
Visually showing byte size of files by creating a tree filled with nodes representing each file within a folder.


Dependencies
-------------

The following packages will need to be installed with pip prior to running the program.

```python
import pygame
import python_ta
```


Running the Program
-------------------
You will have to manually adjust the desired pathing for the folder you wish to look at. 

In ```treemap_visualizer.py```

The following code at the bottom of the file is shown.

```python
if __name__ == '__main__':
    path = '/Users/a16472/Desktop/Balco'
    fst = FileSystemTree(path)
    run_visualisation(fst)
```

Update the <b>path</b> variable to the desired pathing to see the graphical representation of the file sizes within a folder.

Then, simply type 
```python3 treemap_visualizer.py``` in the terminal
to get something like



# Image classifier for recognizing patterns and objects.
## Requirements
- **Python >= 3.2**
- Pandas
- Numpy
- Tensorflow
## Getting started
### Linux
Simply run `python3 main.py` when using Debian/Ubutnu linux distro.
### Windows
The easiest way is to locate your python's location and start it with main.py as an argument.
### Program options
First of all, you will see 3 options:

```
1 - Training
2 - Test labeling
3 - Clear all
```

`Training` is the first option that you should choose when running for the very first time. This command will start creating special filesystem hierarchy in directory `patterns` for tensorflow. Then the program will start learning from the data placed in `resources/decor` directory. This process will be repeated three times for each category: `country`, `decor` and `type`.
This command (if completed successfully) creates new directory `output` where stores cached data.

`Test labeling` is the next command which can be used after learning. This method just takes an image and outputs plaussible results in each of the three categories described above. Your task is to give this command another argument that is a filename of an image to recognize (without an extension, given image must exist in `resources\decor` directory).

`Clear all` command deletes all the data created by the `Training` command. So, it just deletes `patterns` and `output` dirs.

## TO DO
- [ ] Create runner scripts for Win/Linux/MAC OS.
- [ ] Allow png images as an input.
- [ ] Use csv description to create categories instead of creating special filesystem hierarchy.
## Original project
My repo was based on google code labs tutorial at [TensorFlow For Poets](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0).

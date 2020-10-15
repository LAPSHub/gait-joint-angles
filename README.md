# gait-joint-angles
 
Code repository for the LaPS gait analysis laboratory project

Currently, it comprises four scripts:

- `test_script`: this script demonstrates the usage of some `lapsgait` functionalities. 
- `lapsgait`: module with classes and functions to process gait signals.
- *`calcula_angulo`: (deprecated) estimates angles of lower limb joints (hip, knee, and ankle) from points of interest data read from OpenPose output JSON files, segments data from a selection window, interpolates data points, and plots joint graphs;
- `calcula_media`: (deprecated) averages one-gait-cycle segmented angle joint curves.*

The very fist version of these scripts is credited to Frederico Lopes (@fredlopes)

## Requirements

- Python 3.x
- Python modules:
  - os
  - json
  - math
  - matplotlib
  - numpy
  - scipy

## Howto

- `python3 teste_script`

## Contact
- laps@ufpa.br


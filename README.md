# gait-joint-angles
 
Repository for the LaPS gait analysis laboratory project

Currently, it comprises four scripts:

- `calcula_angulo`: estimates angles of lower limb joints (hip, knee, and ankle) from points of interest data read from OpenPose output JSON files, segments data from a selection window, interpolates data points, and plots joint graphs;
- `calcula_media`: averages one-gait-cycle segmented angle joint curves.
- `teste_script`: script created in order to demonstrate the use of the developed module. 
- `lapsgait`: Module with classes and functions for analyze gait signals created from the unification of the calcula_angulo and calcula_media scripts. Keeping the initial objective of both.

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

- `calcula_angulo`
- `calcula_media`
- `teste_script`
- `lapsgait`

## Contact
- laps@ufpa.br


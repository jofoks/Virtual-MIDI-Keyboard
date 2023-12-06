# Virtual MIDI Keyboard

This Python script transforms your computer keyboard into a virtual MIDI controller. It allows you to play musical notes using your keyboard keys, outputting MIDI messages to a virtual MIDI port. This script essentially turns your keyboard into a MIDI keyboard, which can then be used by other music software to create music. It's important to note that this script itself does not provide sound or musical abilities; it simply sends MIDI signals. For actual sound generation and more advanced musical capabilities, please check out my other project [here](https://github.com/jofoks).

## Features

- **Customizable Scales**: Choose from a variety of musical scales including Major, Minor, and Blues.
- **Adjustable Octave**: Set your starting octave to fit your musical needs.
- **Multiple Keyboard Layouts**: Choose from different keyboard layouts (middle, full, upper).
- **Verbosity Levels**: Control the level of output messages.
- **Adjustable Default Velocity**: Set a default velocity for your MIDI notes.

## Installation

Before running the script, ensure you have Python installed on your system. You also need to install the `mido` and `keyboard` libraries. Install them using pip:

```bash
pip install mido keyboard
```

## Usage

Run the script from the command line with the following options:

```
python midi_keyboard.py [OPTIONS]
```

### Options

- `--start_note, -n`: The starting note of the scale (e.g., C). **Required**
- `--scale, -s`: The scale to use (e.g., MAJOR, MINOR). **Required**
- `--octave, -o`: Starting octave (default: 4).
- `--layout, -l`: Keyboard layout (options: middle, full, upper; default: middle).
- `--verbosity, -v`: Verbosity level (0: silent, 1: normal, 2: verbose; default: 1).
- `--default_velocity, -d`: Default velocity for MIDI notes (default: 64).

### Example

```bash
python midi_keyboard.py -n C -s MAJOR -l middle -v 2 -d 80
```

This command starts the MIDI keyboard with C Major scale, middle layout, verbosity level 2, and default velocity of 80.


## TODO:
- Add support for the more message types (other than just note on and off)
- Add functionality to easily shift octaves
- Implement switching and/or passing MIDI channel

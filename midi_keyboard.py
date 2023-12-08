import argparse
import json
from typing import Literal

import itertools
import queue

import mido
import keyboard
from typing import List

Scales = Literal['NONE', 'MAJOR', 'MINOR', 'HARMONIC_MINOR', 'MELODIC_MINOR_ASC', 'BLUES', 'PENTATONIC_MAJOR']

BASE_A4 = 440
NOTES = ('A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#')

SCALES = {
    'NONE': (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    'MAJOR': (2, 2, 1, 2, 2, 2, 1),
    'MINOR': (2, 1, 2, 2, 1, 2, 2),
    'HARMONIC_MINOR': (2, 1, 2, 2, 1, 3, 1),
    'MELODIC_MINOR_ASC': (2, 1, 2, 2, 2, 2, 1),
    'BLUES': (3, 1, 1, 3, 2),
    'PENTATONIC_MAJOR': (2, 2, 3, 2, 3)
}
KEYBOARD_LAYOUTS = {
    'middle': 'a s d f g h j k l ; \''.split(),
    'full': 'a w s e d f t g y h u j k o l p ;\''.split(),
    'upper': 'q w e r t y u i o p [ ] \\'.split(),
}


def scale_generator(start_note: str, scale: Scales, octave: int):
    index = NOTES.index(start_note.upper())

    for step in itertools.cycle(SCALES[scale]):
        yield index + octave * 12
        index += step


class KeyboardMidiDevice:
    def __init__(self,
                 available_keys: List[str],
                 start_note: str,
                 scale: Scales,
                 octave: int = 4,
                 default_velocity: int = 64,
                 output_name: str = None,
                 channel: int = 0
                 ):
        self.default_velocity = default_velocity
        self.output_name = output_name or mido.get_output_names()[0]
        self.midi_port = mido.open_output(name=self.output_name, virtual=False)
        self.message_queue = queue.Queue()
        self.channel = channel

        for key, midi_note in zip(available_keys, scale_generator(start_note, scale, octave)):
            keyboard.on_press_key(key, lambda e, note=midi_note: self._on_key_event(e, note, 'note_on'))
            keyboard.on_release_key(key, lambda e, note=midi_note: self._on_key_event(e, note, 'note_off'))

    def _on_key_event(self, _, note, msg_type):
        midi_msg = mido.Message(msg_type, note=note, velocity=self.default_velocity, channel=self.channel)
        self.midi_port.send(midi_msg)
        self.message_queue.put(midi_msg)

    def __iter__(self):
        while True:
            yield self.message_queue.get()

    def close(self):
        self.midi_port.close()
        keyboard.unhook_all()

    def __del__(self):
        self.close()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Turn your computer keyboard into a MIDI controller.')
    parser.add_argument('--start_note', '-n', type=str, choices=NOTES, default='C',
                        help='The starting note of the scale (e.g., C)')
    parser.add_argument('--scale', '-s', type=str, choices=list(SCALES), default='NONE', help='The scale to use')
    parser.add_argument('--octave', '-o', type=int, default=4, help='Starting octave (default: 4)')
    parser.add_argument('--layout', '-l', type=str, choices=['middle', 'full', 'upper'], default='middle',
                        help='Keyboard layout (default: middle)\n' + json.dumps(KEYBOARD_LAYOUTS))
    parser.add_argument('--verbosity', '-v', type=int, choices=[0, 1, 2], default=1,
                        help='Verbosity level: 0 (silent), 1 (normal), 2 (verbose)')
    parser.add_argument('--default_velocity', '-d', type=int, default=64,
                        help='Default velocity for MIDI notes (default: 64)')
    parser.add_argument('--output', type=str, required=False,
                        help='Name of the MIDI bus to output to, defaults to the first available')
    parser.add_argument('--channel', '-c', type=int, default=0, choices=range(16),
                        help='Channel to send messages on  (default: 0)')
    return parser.parse_args()


def main():
    args = parse_arguments()
    try:
        midi_device = KeyboardMidiDevice(
            available_keys=KEYBOARD_LAYOUTS[args.layout],
            start_note=args.start_note,
            scale=args.scale,
            octave=args.octave,
            default_velocity=args.default_velocity,
            output_name=args.output,
            channel=args.channel
        )

        if args.verbosity >= 1:
            print(
                f"MIDI Controller '{midi_device.output_name}' is sending messages on channel {args.channel}.\n"
                f"Press keys on your keyboard to play notes. Press Ctrl+C to stop."
            )

        for message in midi_device:
            if args.verbosity >= 2:
                print(message)

    except KeyboardInterrupt:
        if args.verbosity >= 1:
            print("MIDI Controller stopped.")


if __name__ == "__main__":
    main()

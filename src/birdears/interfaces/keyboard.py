import urwid
import threading

from .. import INTERVALS

def is_chromatic(key):
    if len(key) == 2:
        return True
    return False

FILL_HEIGHT = 3

def Pad(weight=1):
    return ('weight',
            weight,
            urwid.BoxAdapter(urwid.SolidFill(' '), height=FILL_HEIGHT))

class Key(urwid.WidgetWrap):
    signals = ['click']

    def __init__(self, pitch, top="", middle="", bottom="", *args, **kwargs):
        self.pitch = pitch
        self.pitch_str = str(pitch)
        self.note_str = pitch.note

        if not top:
            top = self.note_str

        text = urwid.Text("{}\n{}\n{}".format(top, middle, bottom))
        fill = urwid.Filler(text)
        adapter = urwid.BoxAdapter(fill, height=FILL_HEIGHT)
        pad = urwid.Padding(adapter)
        box = urwid.LineBox(pad)
        attr = urwid.AttrMap(w=box, attr_map='default')

        super().__init__(attr)

    def highlight(self, state=False):
        attr_map = {None: 'default' if not state else 'highlight'}
        self._w.set_attr_map(attr_map=attr_map)

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            self._emit('click')
            return True
        return False

    def keypress(self, size, key):
        if key in ('enter', ' '):
            self._emit('click')
            return None
        return key

    def selectable(self):
        return True

class Keyboard(urwid.Filler):

    def __init__(self, scale, question_tonic_pitch, main_loop=None,
                 keyboard_index=None, lock=None, *args, **kwargs):

        self.main_loop = main_loop
        self.lock = lock
        self.scale = scale
        self.key_index = {}
        self.highlighted_keys = list()

        chromatic_keys = list()
        diatonic_keys = list()

        if not scale:
             # Handle empty scale if necessary, though unlikely
             super(Keyboard, self).__init__(urwid.SolidFill(' '))
             return

        # Start padding
        start_note = scale[0]
        if is_chromatic(start_note.note):
            diatonic_keys.append(Pad(0.5))
        else:
            chromatic_keys.append(Pad(0.5))

        for i, pitch in enumerate(scale):
            pitch_str = str(pitch)
            note_str = pitch.note

            middle_text = ""
            bottom_text = ""

            if keyboard_index:
                try:
                    _idx = abs(int(question_tonic_pitch) - int(pitch))
                    if _idx < len(keyboard_index):
                         letter = keyboard_index[_idx]
                         # Find interval based on letter index in keyboard_index
                         # We use keyboard_index to find the interval tuple index
                         if letter in keyboard_index:
                             idx_in_keyboard = keyboard_index.index(letter)
                             if idx_in_keyboard < len(INTERVALS):
                                 middle_text = INTERVALS[idx_in_keyboard][1]
                             bottom_text = letter
                except (ValueError, IndexError):
                    pass

            key = Key(pitch=pitch, middle=middle_text, bottom=bottom_text)

            if is_chromatic(note_str):
                chromatic_keys.append(key)
            else:
                diatonic_keys.append(key)
                # Look ahead
                if i + 1 < len(scale):
                    next_pitch = scale[i+1]
                    if not is_chromatic(next_pitch.note):
                        chromatic_keys.append(Pad(1))

        # End padding
        last_pitch = scale[-1]
        if is_chromatic(last_pitch.note):
            diatonic_keys.append(Pad(0.5))
        else:
             chromatic_keys.append(Pad(0.5))

        self.key_index = {str(k.pitch): k
                          for k in chromatic_keys + diatonic_keys
                          if isinstance(k, Key)}

        chromatic_col = urwid.Columns(chromatic_keys, dividechars=1)
        diatonic_col = urwid.Columns(diatonic_keys, dividechars=1)

        pile = urwid.Pile([chromatic_col, diatonic_col])
        box = urwid.LineBox(pile)

        super(Keyboard, self).__init__(body=box, min_height=10, *args, **kwargs)

    def highlight_key(self, element=None):
        if self.lock:
            self.lock.acquire()

        try:
            for key_str in self.highlighted_keys:
                if key_str in self.key_index:
                    self.key_index[key_str].highlight(state=False)
            self.highlighted_keys = []

            if element:
                elem_type = type(element).__name__
                if elem_type == "Pitch":
                    pitch_str = str(element)
                    if pitch_str in self.key_index:
                        self.key_index[pitch_str].highlight(state=True)
                        self.highlighted_keys.append(pitch_str)
                elif elem_type == "Chord":
                    for pitch in element:
                        chord_pitch_str = str(pitch)
                        if chord_pitch_str in self.key_index:
                            self.key_index[chord_pitch_str].highlight(state=True)
                            self.highlighted_keys.append(chord_pitch_str)

            if self.main_loop:
                 self.main_loop.draw_screen()

        finally:
            if self.lock:
                self.lock.release()

import threading

try:
    import urwid
except ImportError:
    from .. import urwid

from .. import KEYS
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT
from .. import INTERVALS

from ..questionbase import QUESTION_CLASSES

from ..note_and_pitch import get_pitch_by_number

from ..scale import ChromaticScale

from .. import D

KEY_PADS = {
    'C#': 1,
    'Db': 1,
    'D#': 0,
    'Eb': 0,
    'F#': 1,
    'Gb': 1,
    'G#': 0,
    'Ab': 0,
    'A#': 0,
    'Bb': 0
}

SPACE_CHAR = ' '
FILL_HEIGHT = 3

LOCK = threading.Lock()


def Pad(weight=1):
    return ('weight',
            weight,
            urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR), height=FILL_HEIGHT))


def is_chromatic(key):
    if len(key) == 2:
        return True
    return False


class KeyboardButton(urwid.Padding):

    signals = ['click']

    def __init__(self, top="", middle="", bottom="", pitch=None, *args,
                 **kwargs):

        self.key_char = bottom
        self.pitch = pitch
        self.pitch_str = str(pitch)
        self.note_str = pitch.note

        top = self.note_str

        text = urwid.Text("{}\n{}\n{}".format(top, middle, bottom))
        fill = urwid.Filler(text)
        adapter = urwid.BoxAdapter(fill, height=3)
        pad = urwid.Padding(adapter)
        pad_attr = urwid.AttrMap(pad, 'default')
        box = urwid.LineBox(pad_attr)
        attr = urwid.AttrMap(w=box, attr_map={None: 'box'})

        super(KeyboardButton, self).__init__(w=attr, *args, **kwargs)

    def highlight(self, state=False):

        if state:
            attr_map = {None: 'highlight', 'default': 'highlight', 'box': 'highlight'}
        else:
            attr_map = {None: 'box', 'default': 'default'}

        self.original_widget.set_attr_map(attr_map=attr_map)

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press' and button == 1:
            urwid.emit_signal(self, 'click', self, self.key_char)
            return True

        return super(KeyboardButton, self).mouse_event(size, event, button, col, row, focus)


class Keyboard(urwid.Filler):

    def __init__(self, scale, question_tonic_pitch, main_loop=None,
                 keyboard_index=None, *args, **kwargs):

        self.main_loop = main_loop

        self.scale = scale

        self.key_index = {}

        self.highlighted_keys = list()

        tonic_pitch = scale[0]
        tonic_str = scale[0].note

        key_scale = [pitch for pitch in scale]

        chromatic_keys = list()
        diatonic_keys = list()

        is_key_chromatic = is_chromatic(key=tonic_str)

        # start (left) padding
        first_pad = diatonic_keys if is_key_chromatic else chromatic_keys
        if tonic_str == "E" or tonic_str == "B":
            first_pad.append(Pad(weight=1.5))
        else:
            first_pad.append(Pad(weight=0.5))

        first_chromatic = [pitch for pitch in key_scale
                           if len(pitch.note) == 2][0]

        for index, pitch in enumerate(key_scale):

            pitch_str = str(pitch)
            note_str = pitch.note

            _idx = abs(int(question_tonic_pitch) - int(pitch))

            letter = keyboard_index[_idx]
            #letter = keyboard_index[index]
            bottom_text = letter
            middle_text = INTERVALS[keyboard_index.index(letter)][1]

            if is_chromatic(pitch.note):

                if KEY_PADS[note_str] == 1 and (pitch is not first_chromatic):
                    chromatic_keys.append(Pad(weight=1))

                chromatic_keys.append(KeyboardButton(pitch=pitch,
                                                     middle=middle_text,
                                                     bottom=bottom_text))

            else:
                diatonic_keys.append(KeyboardButton(pitch=pitch,
                                                    middle=middle_text,
                                                    bottom=bottom_text))

        # end (right) padding:
        if is_key_chromatic:
            weight = 0.5
            diatonic_keys.append(Pad(weight=weight))

        else:

            if KEY_PADS[first_chromatic.note]:
                if tonic_str == "E" or tonic_str == "B":
                    weight = 0.5
                else:
                    weight = (KEY_PADS[first_chromatic.note]/2) + 1
                chromatic_keys.append(Pad(weight=weight))

            if not KEY_PADS[first_chromatic.note]:
                weight = 0.5
                chromatic_keys.append(Pad(weight=weight))

        self.key_index = {item.pitch_str: item
                          for item in chromatic_keys+diatonic_keys
                          if type(item).__name__ == 'KeyboardButton'}

        chromatic = urwid.Columns(widget_list=chromatic_keys, dividechars=1)
        diatonic = urwid.Columns(widget_list=diatonic_keys, dividechars=1)

        keyboard = urwid.Pile([chromatic, diatonic])
        keyboard_attr = urwid.AttrMap(keyboard, 'default')
        box = urwid.LineBox(keyboard_attr)
        box_attr = urwid.AttrMap(box, {None: 'box'})

        super(Keyboard, self).__init__(body=box_attr, min_height=10,
                                       *args, **kwargs)

    def highlight_key(self, element=None):

        with LOCK:

            # for key in self.key_index.values():
            for key in self.highlighted_keys:
                # key.highlight(state=False)
                self.key_index[key].highlight(state=False)
                self.highlighted_keys.remove(key)

        if type(element).__name__ == "Pitch":

            pitch_str = str(element)

            if pitch_str in self.key_index:
                self.key_index[pitch_str].highlight(state=True)
                self.highlighted_keys.append(pitch_str)
                # D(self.highlighted_keys,2)

        elif type(element).__name__ == "Chord":

            for pitch in element:
                chord_pitch_str = str(pitch)

                if chord_pitch_str in self.key_index:
                    self.key_index[chord_pitch_str].highlight(state=True)
                    self.highlighted_keys.append(chord_pitch_str)

        with LOCK:
            self.main_loop.draw_screen()


class TextUserInterfaceWidget(urwid.Frame):

    def __init__(self, *args, **kwargs):

        self.footer_left = urwid.Text('r - Repeat question; q - Quit')
        self.footer_right = urwid.Text('--', align='right')
        header = urwid.AttrMap(urwid.Padding(urwid.Text('birdears ─ Functional'
                                                        ' Ear Training')),
                               'header')
        footer = urwid.AttrMap(urwid.Padding(urwid.Columns(widget_list=[
                            self.footer_left, self.footer_right])), 'footer')
        loading = urwid.Text('loading...')

        adapter = urwid.Filler(loading)

        super(TextUserInterfaceWidget, self).__init__(body=adapter,
                                                      header=header,
                                                      footer=footer)


class QuestionWidget(urwid.Padding):

    def __init__(self, top_widget=None, keyboard=None, bottom_widget=None,
                 display=None, keyboard_width=60, *args, **kwargs):

        top_widget_attr = urwid.AttrMap(top_widget, 'default')
        self.top_widget = urwid.Filler(urwid.AttrMap(urwid.LineBox(top_widget_attr), {None: 'box'}))

        self.keyboard = keyboard

        self.display = dict()

        if not top_widget:
            self.question_text = urwid.Text('..')
            self.top_widget = urwid.Filler(urwid.AttrMap(urwid.LineBox(self.display_text), {None: 'box'}))

        self.display_widget = self.draw_display(question_display=display)

        frame_elements = [self.top_widget, self.keyboard, self.display_widget]
        frame_body = urwid.Pile(widget_list=frame_elements)

        super(QuestionWidget, self).__init__(frame_body, align='center',
                                             width=('relative', keyboard_width))

    def redraw_display(self, question_display):

        self.display_widget = self.draw_display(question_display)

        frame_elements = [self.top_widget, self.keyboard, self.display_widget]
        frame_body = urwid.Pile(widget_list=frame_elements)

        self.original_widget = frame_body

    def draw_display(self, question_display):

        self.display = dict()
        display_wids = list()

        for key, value in question_display.items():
            self.display[key] = urwid.Text(value)
            display_attr = urwid.AttrMap(self.display[key], 'default')
            display_wids.append(urwid.AttrMap(urwid.LineBox(display_attr), {None: 'box'}))

        display_widget = urwid.Filler(urwid.Pile(widget_list=display_wids))

        return display_widget


class TextUserInterface:

    def __init__(self, exercise=None, *args, **kwargs):

        self.exercise = exercise
        self.arguments = kwargs

        self.counter = 0
        self.correct = 0
        self.wrong = 0

        c_text = kwargs.get('color_text', 'default')
        c_bg = kwargs.get('color_bg', 'default')
        c_box = kwargs.get('color_box', 'default')
        c_box_bg = kwargs.get('color_box_bg', 'default')
        c_header_text = kwargs.get('color_header_text', 'light gray')
        c_header_bg = kwargs.get('color_header_bg', 'dark blue')
        c_footer_text = kwargs.get('color_footer_text', 'light gray')
        c_footer_bg = kwargs.get('color_footer_bg', 'dark blue')
        c_highlight_text = kwargs.get('color_highlight_text', 'black')
        c_highlight_bg = kwargs.get('color_highlight_bg', 'light gray')

        palette = [
            ('default', c_text, c_bg),
            ('highlight', c_highlight_text, c_highlight_bg),
            ('header', c_header_text, c_header_bg, '', '#fff', '#336'),
            ('footer', c_footer_text, c_footer_bg, '', '#fff', '#336'),
            ('box', c_box, c_box_bg),
            ]

        self.tui_widget = TextUserInterfaceWidget(*args, **kwargs)

        self.loop = urwid.MainLoop(widget=self.tui_widget, palette=palette)
        self.loop.screen.set_terminal_properties(colors=256)

        try:

            with self.loop.start():

                new_question = True

                while(True):

                    if new_question:

                        self.counter += 1
                        self.create_question(self.exercise, **self.arguments)
                        self.run_question()
                        new_question = False

                    while len(self.input_keys) < self.question.n_input_notes:
                        keys = self.loop.screen.get_input()

                        if not keys:
                            continue

                        input_key = keys[0]

                        if isinstance(input_key, tuple):
                            self.loop.process_input([input_key])
                            continue

                        # these inputs are answers to the exercise
                        if input_key in self.question.keyboard_index \
                           and input_key != ' ':  # space char

                            self.input_keys.append(input_key)
                            if self.question.n_input_notes > 1:
                                self.update_input_display()

                        # these inputs are commands to birdears
                        else:
                            self.keypress(input_key)

                    if self.question.n_input_notes:
                        answer = self.input_keys
                        self.check_question(self.input_keys)

                    new_question = True

        except urwid.ExitMainLoop:
            print("Birdears <https://github.com/iacchus/birdears>")
            print("Exiting...", end="\n\n")
            print("Correct: {} /  Wrong: {}".format(self.correct, self.wrong), end="\n\n")

    def on_key_click(self, button, key_char):
        if key_char in self.question.keyboard_index and key_char != ' ':
            self.input_keys.append(key_char)
            if self.question.n_input_notes > 1:
                self.update_input_display()

    def check_question(self, user_input):

        answer = self.question.check_question(user_input)

        # TODO: UPDATE DISPLAY BEFORE play_resolution
        if answer['is_correct']:
            self.correct += 1
            self.question.display['main_display'] = 'Correct!'
        else:
            self.wrong += 1
            self.question.display['main_display'] = 'Incorrect!'

        answers_text = "Answers: +{correct} / -{incorrect} ".\
            format(correct=self.correct, incorrect=self.wrong)

        self.tui_widget.footer_right.set_text(answers_text)
        self._draw_screen()

        kwargs = {
            'callback': self.keyboard.highlight_key,
            'end_callback': self.keyboard.highlight_key,
        }

        self.question.play_resolution(**kwargs)

        return answer

    def create_question(self, exercise, **kwargs):

        if exercise in QUESTION_CLASSES:
            QUESTION_CLASS = QUESTION_CLASSES[exercise]
        else:
            raise Exception("Invalid `exercise` value:", exercise)

        self.question = QUESTION_CLASS(**kwargs)
        self.question.display.callback = self.update_question_display

        self.input_keys = list()

        self.draw_question()

    def run_question(self):

        kwargs = {
            'callback': self.keyboard.highlight_key,
            'end_callback': self.keyboard.highlight_key,
        }

        self.question.play_question(**kwargs)
        self.keyboard.highlight_key(element=None)

    # TYPES OF DISPLAYS:
    #
    # input_keys (transformed into intervals or notes)
    # str() (displayed literally, overwriting)
    # str() (showing now lines, deleting old ones)
    # list() of str() (showing each str() on a new line)
    # etc
    # Maybe this chould well be an widget feeded by the display dict

    def update_question_display(self):

        for key, value in self.question.display.items():

            if key not in self.question_widget.display:
                self.question_widget.redraw_display(self.question.display)

            self.question_widget.display[key].set_text(value)

        self._draw_screen()

    def update_input_display(self):

        keyboard_index = self.question.keyboard_index

        intervals = [INTERVALS[keyboard_index.index(item)][1]
                     for item in self.input_keys]
        intervals_str = " ".join(intervals)
        self.question.display.update({'input_display': intervals_str})

    def draw_question(self):

        if self.exercise != 'notename':
            scale = \
                ChromaticScale(tonic=self.question.lowest_tonic_pitch.note,
                               octave=self.question.lowest_tonic_pitch.octave,
                               descending=False,
                               n_octaves=self.question.n_octaves)
        else:
            scale = \
                ChromaticScale(tonic=self.question.tonic_str,
                               octave=self.question.lowest_tonic_pitch.octave,
                               n_octaves=self.question.n_octaves)

        self.keyboard = \
            Keyboard(scale=scale,
                     question_tonic_pitch=self.question.tonic_pitch,
                     main_loop=self.loop,
                     keyboard_index=self.question.keyboard_index)

        for key in self.keyboard.key_index.values():
            urwid.connect_signal(key, 'click', self.on_key_click)

        top_variables = {
            'tonic': self.question.tonic_str,
            'mode': self.question.mode.capitalize(),
            'random': ('(random) ' if ('tonic' in self.arguments and
                                       any(el in self.arguments['tonic']
                                       for el in ('r', 'R'))) else ''),
            'descending': self.question.is_descending,
            'chromatic': self.question.is_chromatic,
            'n_octaves': self.question.n_octaves,
            'octaves_str': ('octave' if self.question.n_octaves == 1
                            else 'octaves'),
            'intervals': ", ".join(self.question.allowed_intervals)
        }

        # eg.:
        #
        # Melodic Dictation
        # Key: C Major Descending scale
        # Octaves: 2
        # Chromatics: True
        # Number of notes: 4
        #
        # C Chromatic Descending scale
        # 1 octave

        top_text = "Key: {tonic} {mode} {random}({n_octaves} {octaves_str})\n"\
                   "Descending: {descending}\n" \
                   "Chromatic: {chromatic}\n" \
                   "Intervals: {intervals}" \
                   .format(**top_variables)

        top_widget = urwid.Text(top_text)

        keyboard_width = self.arguments.get('keyboard_width', 60)

        self.question_widget = QuestionWidget(top_widget=top_widget,
                                              keyboard=self.keyboard,
                                              display=self.question.display,
                                              keyboard_width=keyboard_width)

        self.tui_widget.contents.update({'body': (self.question_widget, None)})

        if self.question.n_input_notes > 0:
            answers_text = "Answers: +{correct} / -{incorrect} ".\
                format(correct=self.correct, incorrect=self.wrong)
        else:
            answers_text = "(Question type doesn't takes answer)"
        self.tui_widget.footer_right.set_text(answers_text)

        with LOCK:
            self.loop.draw_screen()

    def keypress(self, key):

        if key in ('T', 't'):
            with LOCK:
                self.loop.screen.clear()
                self.loop.draw_screen()

        elif key in ('R', 'r'):
            self.run_question()

        elif key in ('Q', 'q'):
            raise urwid.ExitMainLoop()

        elif key == 'backspace':
            if len(self.input_keys) > 0:
                self.input_keys.remove(self.input_keys[-1])
                self.update_input_display()
                pass
        else:
            pass

    def _draw_screen(self):
        with LOCK:
            # self.loop.screen.clear()
            self.loop.draw_screen()

            raw_inpt = list(set(self.loop.screen.get_available_raw_input()))
            for item in raw_inpt:
                self.keypress(chr(item))

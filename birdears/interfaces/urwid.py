import threading
import urwid

from .. import KEYS
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT
from .. import INTERVALS

from ..questionbase import QUESTION_CLASSES

from ..note_and_pitch import get_pitch_by_number

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
    
    def __init__(self, top="", middle="", bottom="", pitch=None, *args, **kwargs):
        
        self.pitch = pitch
        self.pitch_str = str(pitch)
        self.note_str = pitch.note
        
        top=self.note_str

        text = urwid.Text("{}\n{}\n{}".format(top, middle, bottom))
        fill = urwid.Filler(text)
        adapter = urwid.BoxAdapter(fill, height=3)
        pad = urwid.Padding(adapter)
        box = urwid.LineBox(pad)
        attr = urwid.AttrMap(w=box, attr_map='default')

        super(KeyboardButton, self).__init__(w=attr, *args, **kwargs)

    def highlight(self, state=False):
        
        attr_map = {None: 'default' if not state else 'highlight'}
        self.original_widget.set_attr_map(attr_map=attr_map)
        
class Keyboard(urwid.Filler):
    
    def __init__(self, scale, main_loop=None, keyboard_index=None, *args, **kwargs):

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
        first_pad.append(Pad(weight=0.5))

        first_chromatic = [pitch for pitch in key_scale if len(pitch.note) == 2][0]

        for index, pitch in enumerate(key_scale):
            
            pitch_str = str(pitch)
            note_str = pitch.note
            
            letter = keyboard_index[index]
            bottom_text = letter
            middle_text = INTERVALS[keyboard_index.index(letter)][1]
            
            if is_chromatic(pitch.note):

                if KEY_PADS[note_str] == 1 and (pitch is not first_chromatic):
                    chromatic_keys.append(Pad(weight=1))

                chromatic_keys.append(KeyboardButton(pitch=pitch, middle=middle_text, bottom=bottom_text))
                
            else:
                diatonic_keys.append(KeyboardButton(pitch=pitch, middle=middle_text, bottom=bottom_text))

        # end (right) padding:
        if is_key_chromatic:
            weight = 0.5 #+ KEY_PADS[first_chromatic] + (int(show_octave)/2)
            diatonic_keys.append(Pad(weight=weight))

        else:

            if KEY_PADS[first_chromatic.note]:
                weight = (KEY_PADS[first_chromatic.note]/2) + 1 #+ int(show_octave)
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
        box = urwid.LineBox(keyboard)
        
        super(Keyboard, self).__init__(body=box, min_height=10, *args, **kwargs)

    def highlight_key(self, element=None):

        with LOCK:
                
            for key in self.key_index.values():
                key.highlight(state=False)
            
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
                #self.key_index[chord_pitch_str].highlight(state=True)
                #self.highlighted_keys.append(chord_pitch_str)
        
        #D(self.highlighted_keys,2)
        with LOCK:
            self.main_loop.draw_screen()


class TextUserInterfaceWidget(urwid.Frame):

    def __init__(self, *args, **kwargs):

        ##header = urwid.AttrMap(urwid.Padding(urwid.Text(('header', 'hey pal'))), 'header')
        ##footer = urwid.AttrMap(urwid.Padding(urwid.Text(('footer', 'footers'))), 'footer')
        self.footer_left = urwid.Text('footers')
        self.footer_right = urwid.Text('--', align='right')
        header = urwid.AttrMap(urwid.Padding(urwid.Text('hey pal')), 'header')
        footer = urwid.AttrMap(
                        urwid.Padding(
                            
                            urwid.Columns(widget_list = 
                            [ self.footer_left,
                            self.footer_right ])
                ), 'footer')
        loading = urwid.Text('loading...')
        
        adapter = urwid.Filler(loading)

        super(TextUserInterfaceWidget, self).__init__(body=adapter, header=header, footer=footer)


class QuestionWidget(urwid.Padding):
    
    def __init__(self, top_widget=None, keyboard=None, bottom_widget=None, *args, **kwargs):
        
        self.top_widget = urwid.Filler(urwid.LineBox(top_widget))
        
        if not top_widget:
            self.question_text = urwid.Text('..')
            self.top_widget = urwid.Filler(urwid.LineBox(self.display_text))
            
        if not bottom_widget:
            self.display_text = urwid.Text('-')
            self.bottom_widget = urwid.Filler(urwid.LineBox(self.display_text))

        frame_elements = [self.top_widget, keyboard, self.bottom_widget]
        frame_body = urwid.Pile(widget_list=frame_elements)
        
        super(QuestionWidget, self).__init__(frame_body, align='center', width=('relative', 60))
    

class TextUserInterface:
    
    def __init__(self, exercise, *args, **kwargs):
        
        self.exercise = exercise
        self.arguments = kwargs
        
        self.correct = 0
        self.wrong = 0
        
        palette = [
            ('default', 'default', 'default'),
            ('highlight', 'black', 'light gray'),
            ('header', 'light gray', 'dark blue','','#fff','#336'),
            ('footer', 'light gray', 'dark blue','','#fff','#336'),
            ]
        
        self.tui_widget = TextUserInterfaceWidget(*args, **kwargs)
        
        self.loop = urwid.MainLoop(widget=self.tui_widget, palette=palette)
        self.loop.screen.set_terminal_properties(colors=256)
        
        with self.loop.start():
            
            new_question = True
        
            while(True):
                
                if new_question:
                
                    self.run_question()
                    new_question = False
                    
                self.loop.screen.get_available_raw_input()
                
                # for i in range(self.question.n_input_notes): #etc
                # FIXME: please refactor
                if self.question.name != 'instrumental':
                    
                    #with LOCK:
                    #user_input = self.loop.screen.get_input()[0]
                    user_input = self.loop.screen.get_input()[0]
                    
                    # these inputs are answers to the exercise 
                    if user_input in self.question.keyboard_index and user_input != ' ': # space char
                        
                        self.input_keys.append(user_input)
                        #self.update_input_wid()
                        
                        if len(self.input_keys) == self.question.n_notes:
                            
                            answer = self.input_keys if self.question.n_notes > 1 else user_input 
                            self.check_question(answer)
                            
                            new_question = True
                            
                    # these inputs are commands to birdears 
                    else:
                        self.keypress(user_input[0] if type(user_input) == list else user_input)
                        
                # instrumental doesn't take input
                else:
                    for r in range(self.question.n_repeats):
                        self.question.play_question()

                        for i in range(self.question.wait_time):
                            time_left = str(self.question.wait_time - i).rjust(3)
                            text = '{} seconds remaining...'.format(time_left)
                            #print(center_text(text, sep=False), end='')
                            with LOCK:
                                self.question.question._wait(1)
                            
                            user_input = self.loop.screen.get_available_raw_input()
                            if user_input:
                                self.keypress(user_input[0] if type(user_input) == list else user_input)
                    
                    new_question = True
                
    def check_question(self, user_input):
        
        answer = self.question.check_question(user_input)
        
        # TODO: UPDATE DISPLAY BEFORE play_resolution
        if answer['is_correct']:
            self.correct += 1
        else:
            self.wrong += 1
            
        answers_text = "Answers: +{correct} / -{incorrect} ".\
            format(correct=self.correct, incorrect=self.wrong)
        #self.input_wid = urwid.Text('')
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
            raise Exception("Oops!", QUESTION_CLASSES)

        return QUESTION_CLASS(**kwargs)


    def run_question(self):

        self.question = self.create_question(exercise=self.exercise, **self.arguments)
        self.question.display.callback = self.update_question_display
        #D(self.question.n_notes)
        self.input_keys = list()

        self.draw_question()

        kwargs = {
            'callback': self.keyboard.highlight_key,
            'end_callback': self.keyboard.highlight_key,
        }

        self.question.play_question(**kwargs)
        
    def update_question_display(self):
        text = str()
        # FIXME
        for value in self.question.display.values():
            text += value
        self.question_widget.display_text.set_text(str(text))
        self._draw_screen()

    def draw_question(self):

        self.keyboard = Keyboard(scale=self.question.chromatic_scale, main_loop=self.loop, 
                            keyboard_index=self.question.keyboard_index)
        
        top_variables = {
            'tonic': self.question.tonic_str + (' (random)' if any(el in self.arguments['tonic'] for el in ('r', 'R')) else ''),
            'descending': self.question.is_descending,
            'chromatic': self.question.is_chromatic,
        }
        
        top_text = """\
Tonic: {tonic}
Descending: {descending} Chromatic: {chromatic}\
        """.format(**top_variables)
        
        top_widget = urwid.Text(top_text)
        
        #self.input_wid = urwid.Text('')
        #bottom_widget = urwid.Text('please write me!!!')
        
        #self.question_widget = QuestionWidget(top_widget=top_widget, keyboard=self.keyboard, bottom_widget=bottom_widget)
        self.question_widget = QuestionWidget(top_widget=top_widget, keyboard=self.keyboard)
        
        self.tui_widget.contents.update({'body': (self.question_widget, None)})
        
        answers_text = "Answers: +{correct} / -{incorrect} ".\
            format(correct=self.correct, incorrect=self.wrong)
        self.tui_widget.footer_right.set_text(answers_text)
        
        with LOCK:
            self.loop.draw_screen()

    def keypress(self, key):
        
        if key in ('T', 't'):
            with LOCK:
                self.loop.screen.clear()
                self.loop.draw_screen()
            
        elif key in ('R', 'r'):
            kwargs = {
                'callback': self.keyboard.highlight_key,
                'end_callback': self.keyboard.highlight_key,
            }

            self.question.play_question(**kwargs)
            
        elif key in ('Q', 'q'):
            raise urwid.ExitMainLoop()
        
        elif key == 'backspace':
            if len(self.input_keys) > 0:
                #self.update_input_wid()
                pass
        else:
            pass
        
    def _draw_screen(self):
        with LOCK:
            #self.loop.screen.clear()
            self.loop.draw_screen()

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
    
    def __init__(self, scale, main_loop=None, *args, **kwargs):

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

        for pitch in key_scale:
            
            pitch_str = str(pitch)
            note_str = pitch.note
            
            if is_chromatic(pitch.note):

                if KEY_PADS[note_str] == 1 and (pitch is not first_chromatic):
                    chromatic_keys.append(Pad(weight=1))

                chromatic_keys.append(KeyboardButton(pitch=pitch))
                
            else:
                diatonic_keys.append(KeyboardButton(pitch=pitch))

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
            #chord = element
            
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

        header = urwid.Text('hey pal')
        footer = urwid.Text('footers')
        loading = urwid.Text('loading...')
        
        adapter = urwid.Filler(loading)

        super(TextUserInterfaceWidget, self).__init__(body=adapter, header=header, footer=footer)


class QuestionWidget(urwid.Padding):
    
    def __init__(self, top_widget, keyboard, bottom_widget, *args, **kwargs):
        
        ##top_widget = urwid.Filler(urwid.LineBox(urwid.Text('test1\nok')))
        ##bottom_widget = urwid.Filler(urwid.LineBox(urwid.Text('test2')))
        top_widget = urwid.Filler(urwid.LineBox(top_widget))
        bottom_widget = urwid.Filler(urwid.LineBox(bottom_widget))

        frame_elements = [top_widget, keyboard, bottom_widget]
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
            ('highlight', 'black', 'light gray')
            ]
        
        self.tui_widget = TextUserInterfaceWidget(*args, **kwargs)
        
        #self.loop = urwid.MainLoop(widget=self.tui_widget, palette=palette, unhandled_input=self.keypress)
        self.loop = urwid.MainLoop(widget=self.tui_widget, palette=palette)
        
        with self.loop.start():
            
            new_question = True
        
            while(True):
                if new_question:
                    self.run_question()
                    new_question = False
                    
                self.loop.screen.get_available_raw_input()
                # FIXME: please refactor
                if self.question.name != 'instrumental':
                    user_input = self.loop.screen.get_input()[0]
                    
                    if user_input in self.question.keyboard_index and user_input != ' ': # space char
                        self.input_keys.append(user_input)
                        #self.tui_widget.contents['body'][0].original_widget.contents[0] = (urwid.Text(str(self.input_keys)),('pack',None))
                        self.update_input_wid()
                        #self._draw_screen()
                        if len(self.input_keys) == self.question.n_notes:
                            answer = self.input_keys if self.question.n_notes > 1 else user_input 
                            #D(answer,2)
                            self.check_question(answer)
                            new_question = True
                    else:
                        self.keypress(user_input[0] if type(user_input) == list else user_input)
                # instruental doesn't take input
                else:
                    new_question = True
                
    def check_question(self, user_input):
        
        #answer = self.question.check_question(user_input_char=user_input)
        answer = self.question.check_question(user_input)
        
        if answer['is_correct']:
            self.correct += 1
        else:
            self.wrong += 1
            
            
        kwargs = {
            'callback': self.tui_widget['body'].contents[1][0].highlight_key,
            'end_callback': self.tui_widget['body'].contents[1][0].highlight_key,
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
        D(self.question.n_notes)
        self.input_keys = list()

        self.draw()

        kwargs = {
            'callback': self.tui_widget['body'].contents[1][0].highlight_key,
            'end_callback': self.tui_widget['body'].contents[1][0].highlight_key,
        }

        self.question.play_question(**kwargs)

    def update_input_wid(self):
        key_index = self.question.keyboard_index
        
        input_list = [INTERVALS[key_index.index(key)][1] for key in self.input_keys]
        input_display = " ".join(input_list)
        self.input_wid.set_text(input_display)
        self._draw_screen()
            
    def draw(self):

        keyboard = Keyboard(scale=self.question.chromatic_scale, main_loop=self.loop)
        
        
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
        
        ###bottom_text = """
        ###Answers: +{correct} / -{incorrect}
        ###""".format(correct=self.correct, incorrect=self.wrong)
        answers_text = "Answers: +{correct} / -{incorrect} ".\
            format(correct=self.correct, incorrect=self.wrong)
        self.input_wid = urwid.Text('')
        bottom_widget = urwid.Columns(widget_list=[self.input_wid,
                                                   urwid.Text(markup=answers_text, align='right')])
        
        self.question_widget = QuestionWidget(top_widget=top_widget, keyboard=keyboard, bottom_widget=bottom_widget)
        
        self.tui_widget.contents.update({'body': (self.question_widget, None)})
        
        with LOCK:
            self.loop.draw_screen()

    def keypress(self, key):
        
        D(key)

        if key in ('T', 't'):
            with LOCK:
                self.loop.screen.clear()
                self.loop.draw_screen()
            
        elif key in ('R', 'r'):
            kwargs = {
                'callback': self.tui_widget['body'].contents[1][0].highlight_key,
                'end_callback': self.tui_widget['body'].contents[1][0].highlight_key,
            }

            self.question.play_question(**kwargs)
            
        elif key in ('Q', 'q'):
            raise urwid.ExitMainLoop()
        
        elif key == 'backspace':
            if len(self.input_keys) > 0:
                self.update_input_wid()
        else:
            pass
        
    def _draw_screen(self):
        with LOCK:
            self.loop.screen.clear()
            self.loop.draw_screen()

import threading
import urwid

from .. import KEYS
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT

from ..questionbase import QUESTION_CLASSES

from ..note_and_pitch import get_pitch_by_number

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
        attr = urwid.AttrMap(w=pad, attr_map='default')

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

        from .. import D
        
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
    
    def __init__(self, keyboard, *args, **kwargs):
        
        top_widget = urwid.Filler(urwid.LineBox(urwid.Text('test1\nok')))
        bottom_widget = urwid.Filler(urwid.LineBox(urwid.Text('test2')))

        frame_elements = [top_widget, keyboard, bottom_widget]
        frame_body = urwid.Pile(widget_list=frame_elements)
        
        super(QuestionWidget, self).__init__(frame_body, align='center', width=('relative', 60))
    

class TextUserInterface:
    
    def __init__(self, exercise, *args, **kwargs):
        
        self.exercise = exercise
        self.arguments = kwargs
        
        palette = [
            ('default', 'default', 'default'),
            ('highlight', 'black', 'light gray')
            ]
        
        self.tui_widget = TextUserInterfaceWidget(*args, **kwargs)
        
        self.loop = urwid.MainLoop(widget=self.tui_widget, palette=palette, unhandled_input=self.keypress)
        
        with self.loop.start():
            while(True):
                self.run_question()
        
    def create_question(self, exercise, **kwargs):

        if exercise in QUESTION_CLASSES:
            QUESTION_CLASS = QUESTION_CLASSES[exercise]
        else:
            raise Exception("Oops!", QUESTION_CLASSES)

        if 'n_notes' in kwargs:
            dictate_notes = kwargs['n_notes']
        else:
            dictate_notes = 1

        return QUESTION_CLASS(**kwargs)


    def run_question(self):

        self.question = self.create_question(exercise=self.exercise, **self.arguments)

        self.input_keys = list()

        self.draw(self.question)

        kwargs = {
            'callback': self.tui_widget['body'].contents[1][0].highlight_key,
            'end_callback': self.tui_widget['body'].contents[1][0].highlight_key,
        }

        #self.thread = threading.Thread(target=self.question.play_question, kwargs=kwargs)
        #self.thread.start()
        #self.thread.join()

        self.question.play_question(**kwargs)

    def draw(self, question):

        keyboard = Keyboard(scale=question.chromatic_scale, main_loop=self.loop)

        self.question_widget = QuestionWidget(keyboard=keyboard)
        
        self.tui_widget.contents.update({'body': (self.question_widget, None)})
        #if len(self.loop) > 0:
        
        with LOCK:
            self.loop.draw_screen()

    def keypress(self, key):

        if key in self.question.keyboard_index and key != ' ': # space char
            self.input_keys.append(key)

            response = self.question.check_question(self.input_keys)
            #print_response(response)

            kwargs = {
                'callback': self.frame_body.contents[1][0].highlight_key,
                'end_callback': self.frame_body.contents[1][0].highlight_key,
                'ui_obj': self
            }

            #self.thread = threading.Thread(target=self.question.play_resolution, kwargs=kwargs)
            #self.thread.start()
            #self.thread.join()

            self.question.play_resolution(**kwargs)
            
            self.run_question()
            # self.question.play_resolution()

        elif key in ('T', 't'):
            with LOCK:
                self.loop[0].draw_screen()
            
        elif key in ('R', 'r'):
            kwargs = {
                'callback': self.frame_body.contents[1][0].highlight_key,
                'end_callback': self.frame_body.contents[1][0].highlight_key,
                'ui_obj': self
            }

            self.thread = threading.Thread(target=self.question.play_question, kwargs=kwargs)
            self.thread.start()
            self.thread.join()
            #self.question.play_question()
            
        elif key in ('Q', 'q'):
            raise urwid.ExitMainLoop()
        else:
            pass

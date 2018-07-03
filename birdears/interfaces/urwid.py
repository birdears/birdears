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

        for highlighted in self.highlighted_keys:
            self.key_index[highlighted].highlight(state=False)
            self.highlighted_keys.remove(highlighted)
            
        if type(element).__name__ == "Pitch":
            #with open('dbg_pipe', 'w') as pipe:
            #    pipe.write(str(type(element).__name__))
            pitch = element
            pitch_str = str(pitch)
            
            # turn off other highlighted keys
            #for highlighted in self.highlighted_keys:
            #    self.key_index[highlighted].highlight(state=False)
            #    self.highlighted_keys.remove(highlighted)
                
            if pitch_str in self.key_index:
                self.key_index[pitch_str].highlight(state=True)
                self.highlighted_keys.append(pitch_str)
            
        elif type(element).__name__ == "Chord":
            chord = element
            
            # turn off other highlighted keys
            #for highlighted in self.highlighted_keys:
            #    self.key_index[highlighted].highlight(state=False)
            #    self.highlighted_keys.remove(highlighted)
                
            for pitch in chord:
                chord_pitch_str = str(pitch)
                
                if chord_pitch_str in self.key_index:
                    self.key_index[chord_pitch_str].highlight(state=True)
                    self.highlighted_keys.append(chord_pitch_str)
            
        else:
            pass
        #elif type(element).__name__ == "NoneType":
            # turn off all highlighted keys when 'element' == 'None'
            #for highlighted in self.highlighted_keys:
            #    self.highlighted_keys.remove(highlighted)
            #    self.key_index[highlighted].highlight(state=False)
            
        #elif type(element).__name__ == "Chord":
         
        # FIXME: think on a better solution for this loop
        #for key, button in self.key_index.items():

        #    state = (key == str(pitch))
        #    button.highlight(state=state)
            
        if len(self.main_loop) > 0:
            self.main_loop[0].draw_screen()


class TextUserInterface(urwid.Frame):

    def __init__(self, exercise, loop_wrapper, *args, **kwargs):

        
        self.loop = loop_wrapper
        header = urwid.Text('hey pal')
        footer = urwid.Text('footers')
        loading = urwid.Text('loading...')
        adapter = urwid.Filler(loading)

        super(TextUserInterface, self).__init__(body=adapter, header=header, footer=footer)
        self.exercise = exercise
        self.kwargs = kwargs

        self.run_question()

    def run_question(self):

        self.question = self.create_question(exercise=self.exercise, **self.kwargs)

        self.input_keys = list()

        self.draw(self.question)

        kwargs = {
            'callback': self.frame_body.contents[1][0].highlight_key,
            'end_callback': self.frame_body.contents[1][0].highlight_key
        }

        self.thread = threading.Thread(target=self.question.play_question, kwargs=kwargs)
        self.thread.start()
        self.thread.join()

        #self.question.play_question(**kwargs)

    def keypress(self, size, key):

        if key in self.question.keyboard_index and key != ' ': # space char
            self.input_keys.append(key)

            response = self.question.check_question(self.input_keys)
            #print_response(response)

            kwargs = {
                'callback': self.frame_body.contents[1][0].highlight_key,
                'end_callback': self.frame_body.contents[1][0].highlight_key,
            }

            thread = threading.Thread(target=self.question.play_resolution, kwargs=kwargs)
            thread.start()
            thread.join()

            self.run_question()
            # self.question.play_resolution()

        elif key in ('T', 't'):
            self.loop[0].draw_screen()
            
        elif key in ('R', 'r'):
            kwargs = {
                'callback': self.frame_body.contents[1][0].highlight_key,
                'end_callback': self.frame_body.contents[1][0].highlight_key
            }

            self.thread = threading.Thread(target=self.question.play_question, kwargs=kwargs)
            self.thread.start()
            self.thread.join()
            #self.question.play_question()
            
        elif key in ('Q', 'q'):
            raise urwid.ExitMainLoop()
        else:
            pass

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

    def draw(self, question):

        # keyboard = Keyboard(tonic=question.tonic_str, main_loop=self.loop)
        keyboard = Keyboard(scale=question.chromatic_scale, main_loop=self.loop)

        top_widget = urwid.Filler(urwid.LineBox(urwid.Text('test1\nok')))
        bottom_widget = urwid.Filler(urwid.LineBox(urwid.Text('test2')))

        frame_elements = [top_widget, keyboard, bottom_widget]

        self.frame_body = urwid.Pile(widget_list=frame_elements)
        self.frame_body_pad = urwid.Padding(self.frame_body, align='center', width=('relative', 60))

        self.contents.update({'body': (self.frame_body_pad, None)})

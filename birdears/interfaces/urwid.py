import urwid

from .. import KEYS
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT

from ..questionbase import QUESTION_CLASSES

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

def is_chromatic(key):
    if len(key) == 2:
        return True
    return False

class KeyboardButton(urwid.Padding):
    def __init__(self, top="", middle="", bottom="", *args, **kwargs):
        text = [urwid.Text(str(item)) for item in [top, middle, bottom]]
        lines = urwid.Pile(text)
        fill = urwid.Filler(lines)
        adapter = urwid.BoxAdapter(fill, height=3)
        pad = urwid.Padding(adapter)
        box = urwid.LineBox(pad)
        
        super(KeyboardButton, self).__init__(w=box, *args, **kwargs)
        
class Keyboard(urwid.Filler):
    def __init__(self, tonic, show_octave=True, *args, **kwargs):
        
        if tonic in KEYS:
            scale = CHROMATIC_SHARP if tonic in CHROMATIC_SHARP else CHROMATIC_FLAT
            idx = scale.index(tonic)
            key_scale = scale[idx:] + scale[:idx]
            
        chromatic_keys = list()
        diatonic_keys = list()

        is_key_chromatic = is_chromatic(tonic)
        
        if is_key_chromatic:
            diatonic_keys.append(('weight', 0.5, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
        else:
            chromatic_keys.append(('weight', 0.5, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
        
        first_chromatic = [note for note in key_scale if len(note) == 2][0]
        # last_chromatic = [note for note in key_scale if len(note) == 2][-1]
        
        for idx, note in enumerate(key_scale):
            
            if is_chromatic(note):
                
                if KEY_PADS[note] == 1 and note != first_chromatic:
                    chromatic_keys.append(('weight', 1, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
                    
                chromatic_keys.append(('weight', 1, KeyboardButton(note)))
            
            else:
                diatonic_keys.append(KeyboardButton(note))
                
        if show_octave:
            if is_chromatic(tonic):
                if KEY_PADS[tonic] == 1:
                    chromatic_keys.append(('weight', 1, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
                chromatic_keys.append(('weight', 1, KeyboardButton(tonic)))
            else:
                diatonic_keys.append(KeyboardButton(tonic))
                
        if is_key_chromatic:
            if not show_octave:
                weight = 0.5 + KEY_PADS[first_chromatic] + (int(show_octave)/2)
                chromatic_keys.append(('weight', weight, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
            else:
                weight = 0.5 #+ KEY_PADS[first_chromatic] + (int(show_octave)/2)
                diatonic_keys.append(('weight', weight, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
            
        else:
            
            if KEY_PADS[first_chromatic]:
                weight = (KEY_PADS[first_chromatic]/2) + int(show_octave)
                chromatic_keys.append(('weight', weight, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
            
            if not KEY_PADS[first_chromatic]:
                if not show_octave:
                    weight = 0.5 + KEY_PADS[first_chromatic] + int(show_octave)
                    diatonic_keys.append(('weight', weight, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
                else:
                    weight = 0.5 #+ KEY_PADS[first_chromatic] + int(show_octave)
                    chromatic_keys.append(('weight', weight, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))

        chromatic = urwid.Columns(widget_list=chromatic_keys, dividechars=1)
        diatonic = urwid.Columns(widget_list=diatonic_keys, dividechars=1)
        
        keyboard = urwid.Pile([chromatic, diatonic])
        box = urwid.LineBox(keyboard)
        
        super(Keyboard, self).__init__(body=box, min_height=6, *args, **kwargs)
        


class TextUserInterface(urwid.Frame):

    def __init__(self, exercise, *args, **kwargs):

        self.question = self.create_question(exercise=exercise, **kwargs)
        
        self.input_keys = list()
        
        import threading

        thread = threading.Thread(target=self.question.play_question)
        thread.start()
        self.draw(self.question)
        #thread = self.question.pre_question.play()
        #thread.join()
        #thread = self.question.question.play()
        #thread.join()
        
        loop = urwid.MainLoop(self)
        loop.run()
        
    def keypress(self, size, key):
        #print(size, key)
        if key in self.question.keyboard_index and key != ' ': # space char
            self.input_keys.append(key)

            #if exercise == 'dictation':
            #    input_str = make_input_str(input_keys, question.keyboard_index)
            #    #print(input_str, end='')

            #if len(input_keys) == dictate_notes:

            response = self.question.check_question(self.input_keys)
            #print_response(response)

            self.question.play_resolution()

                #new_question_bit = True
        elif key in ('R', 'r'):
            self.question.play_question()
        elif key in ('Q', 'q'):
            raise urwid.ExitMainLoop()
        else:
            pass
        
        #self.keyboard = Keyboard(tonic='D')
        
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
        
        self.header = urwid.Text('hey pal')
        self.footer = urwid.Text('footers')

        self.keyboard = Keyboard(tonic='C')
        self.keyboard = Keyboard(question.tonic_str)
        
        self.top_widget = urwid.Filler(urwid.LineBox(urwid.Text('test1')))
        self.bottom_widget = urwid.Filler(urwid.LineBox(urwid.Text('test2')))
        
        self.frame_elements = [self.top_widget, self.keyboard, self.bottom_widget]
        
        self.frame_body = urwid.Pile(widget_list=self.frame_elements)
        self.frame_body_pad = urwid.Padding(self.frame_body, align='center', width=('relative', 60))

        super(TextUserInterface, self).__init__(body=self.frame_body_pad, header=self.header, footer=self.footer)

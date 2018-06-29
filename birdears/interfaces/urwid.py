import urwid

from .. import KEYS
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT

#KEYS = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#',
#        'Ab', 'A', 'A#', 'Bb', 'B')

#CHROMATIC_SHARP = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#',
#                   'B')

#CHROMATIC_FLAT = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb',
#                  'B')

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
    def __init__(self, tonic='F#', show_octave=True, *args, **kwargs):
        
        if tonic in KEYS:
            scale = CHROMATIC_SHARP if tonic in CHROMATIC_SHARP else CHROMATIC_FLAT
            idx = scale.index(tonic)
            key_scale = scale[idx:] + scale[:idx]
            
            
        print(key_scale)
        
        chromatic_keys = list()
        diatonic_keys = list()

        is_key_chromatic = is_chromatic(tonic)
        
        if is_key_chromatic:
            diatonic_keys.append(('weight', 0.5, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
        else:
            chromatic_keys.append(('weight', 0.5, urwid.BoxAdapter(urwid.SolidFill(SPACE_CHAR),height=1)))
        
        first_chromatic = [note for note in key_scale if len(note) == 2][0]
        last_chromatic = [note for note in key_scale if len(note) == 2][-1]
        
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

    def __init__(self, *args, **kwargs):

        header = urwid.Text('hey pal')
        footer = urwid.Text('footers')

        keyboard = Keyboard()
        
        top_widget = urwid.Filler(urwid.LineBox(urwid.Text('test1')))
        bottom_widget = urwid.Filler(urwid.LineBox(urwid.Text('test2')))
        
        frame_elements = [top_widget, keyboard, bottom_widget]
        
        frame_body = urwid.Pile(widget_list=frame_elements)
        frame_body_pad = urwid.Padding(frame_body, align='center', width=('relative', 60))

        super(TextUserInterface, self).__init__(body=frame_body_pad, header=header, footer=footer, *args, **kwargs)


def TextUserInterface(exercise, *args, **kwargs):
    
    if exercise == 'dictation':
        from ..questions.melodicdictation import MelodicDictationQuestion
        dictate_notes = kwargs['n_notes']
        MYCLASS = MelodicDictationQuestion

    elif exercise == 'instrumental':
        from ..questions.instrumentaldictation \
            import InstrumentalDictationQuestion

        dictate_notes = kwargs['n_notes']
        MYCLASS = InstrumentalDictationQuestion

    elif exercise == 'melodic':
        from ..questions.melodicinterval import MelodicIntervalQuestion
        MYCLASS = MelodicIntervalQuestion
        dictate_notes = 1

    elif exercise == 'notename':
        from ..questions.notename import NoteNameQuestion
        MYCLASS = NoteNameQuestion
        dictate_notes = 1

    elif exercise == 'harmonic':
        from ..questions.harmonicinterval import HarmonicIntervalQuestion
        MYCLASS = HarmonicIntervalQuestion
        dictate_notes = 1
        
    question = MYCLASS(**kwargs)
        
    keyb = Keyboard()
    #fill = urwid.Filler(txt, 'top')
    pad = urwid.Padding(keyb, align='center', width=('relative', 60))
    loop = urwid.MainLoop(pad)
    loop.run()

from random import randrange
from random import choice

from . import KEYBOARD_INDICES
from . import CHROMATIC_TYPE
from . import KEYS
from . import DEGREE_INDEX

# from .interval import Interval

from .note_and_pitch import Pitch

from .scale import DiatonicScale
from .scale import ChromaticScale

from functools import wraps

QUESTION_CLASSES = {}


class DictCallback(dict):
    
    callback = None
    
    callback_args = list()
    callback_kwargs = dict()
    
    def __init__(self, other=None, **kwargs):
        #super(DictCallback, self).__init__(self, other, **kwargs)
        super(DictCallback, self).__init__()
        self.update(other)
        
    def __setitem__(self, key, value):
        super(DictCallback, self).__setitem__(self, key, value)
        
        if self.callback:
            self.callback(*self.callback_args, **self.callback_kwargs)
            
    def update(self, other=None):
        super(DictCallback, self).update(other)
        
        if self.callback:
            self.callback(*self.callback_args, **self.callback_kwargs)
        
def register_question_class(cls, *args, **kwargs):
    """Decorator for question classes.

    Classes decorated with this decorator will be registered in the
    `QUESTION_CLASSES` global.
    """

    global QUESTION_CLASSES
    
    QUESTION_CLASSES.update({cls.name: cls})
    
    return cls


# values for valid_semitones list can be Interval objects or int's (semitones)
def get_valid_pitches(scale, valid_intervals=CHROMATIC_TYPE):
    
    tonic_pitch = scale[0]

    valid_scale = list()

    if isinstance(valid_intervals, tuple):
        valid_list = list(map(lambda x: str(x), valid_intervals))
    elif isinstance(valid_intervals, list):
        valid_list = list(map(lambda x: str(x), valid_intervals))
    elif isinstance(valid_intervals, str):
        valid_list = valid_intervals.replace(' ', '').split(',')
    else:
        raise Exception('Incorrect type for valid_semitones')

    valid_semitones = list()

    for item in valid_list:

        # 'i', 'ii' etc...
        if item.lower() in DEGREE_INDEX:
            valid_semitones.extend(DEGREE_INDEX[item.lower()])
        # 0, 1, 2 etc...
        elif item.isdecimal():
            valid_semitones.append(int(item))
        # something else
        else:
            print('Warning: invalid `valid_interval`: ', item)
            continue

    for pitch in scale:

        # this will work with multple octaves
        chromatic_offset = \
            abs(int(tonic_pitch) - int(pitch)) % 12

        if chromatic_offset in valid_semitones:
            valid_scale.append(pitch)

    return valid_scale


class QuestionBase:
    """
    Base Class to be subclassed for Question classes.

    This class implements attributes and routines to be used in Question
    subclasses.
    """

    def __init__(self, mode='major', tonic='C', octave=4, descending=False,
                 chromatic=False, n_octaves=1, valid_intervals=CHROMATIC_TYPE,
                 user_durations=None, prequestion_method=None,
                 resolution_method=None, default_durations=None,
                 *args, **kwargs):
        """Inits the class.

        Args:
            mode (str): A string represnting the mode of the question.
                Eg., 'major' or 'minor'
            tonic (str): A string representing the tonic of the
                question, eg.: 'C'; if omitted, it will be selected
                randomly.
            octave (int): A scienfic octave notation, for example,
                4 for 'C4'; if not present, it will be randomly chosen.
            descending (bool): Is the question direction in descending,
                ie., intervals have lower pitch than the tonic.
            chromatic (bool): If the question can have (True) or not
                (False) chromatic intervals, ie., intervals not in the
                diatonic scale of tonic/mode.
            n_octaves (int): Maximum numbr of octaves of the question.
            valid_intervals (list): A list with intervals (int) valid for
                random choice, 1 is 1st, 2 is second etc. Eg. [1, 4, 5] to
                allow only tonics, fourths and fifths.
            user_durations (str): A string with 9 comma-separated `int` or
                `float`s to set the default duration for the notes played. The
                values are respectively for: pre-question duration (1st),
                pre-question delay (2nd), and pre-question pos-delay (3rd);
                question duration (4th), question delay (5th), and question
                pos-delay (6th); resolution duration (7th), resolution
                delay (8th), and resolution pos-delay (9th).
                duration is the duration in of the note in seconds; delay is
                the time to wait before playing the next note, and pos_delay is
                the time to wait after all the notes of the respective sequence
                have been played. If any of the user durations is `n`, the
                default duration for the type of question will be used instead.
                Example::
                    "2,0.5,1,2,n,0,2.5,n,1"
            prequestion_method (str): Method of playing a cadence or the
                exercise tonic before the question so to affirm the question
                musical tonic key to the ear. Valid ones are registered in the
                `birdears.prequestion.PREQUESION_METHODS` global dict.
            resolution_method (str): Method of playing the resolution of an
                exercise Valid ones are registered in the
                `birdears.resolution.RESOLUTION_METHODS` global dict.
            user_durations (dict): Dictionary with the default durations for
                each type of sequence. This is provided by the subclasses.
        """

        self.display = DictCallback({'main_display': str()})
        
        self.mode = mode

        self.is_descending = descending
        self.is_chromatic = chromatic
        
        try:
            if kwargs['n_notes']:
                self.n_notes = kwargs['n_notes']
        except KeyError:
            self.n_notes = 1

        # self.octave = octave if octave else randrange(3, 5)
        if isinstance(octave, str) and any(el in octave for el in ('R', 'r')):
            self.octave = randrange(3, 6)
        elif isinstance(octave, str) and ',' in octave:
            octave = octave.replace(' ', '')
            octave = choice(octave.split(','))
            self.octave = int(octave)
        elif isinstance(octave, int) and (octave >= 3 and octave <= 6):
            self.octave = octave
        elif isinstance(octave, list):
            self.octave = int(choice(octave))
        elif isinstance(octave, tuple) and len(octave) == 2:
            self.octave = randrange(*octave)
        # if not octave:
        else:
            self.octave = randrange(3, 6)

        # TODO: raise exceptions in case octave/n_octaves are invalid or
        #       extrapolate each other

        # self.octave = octave

        self.n_octaves = n_octaves

        direction = 'descending' if descending else 'ascending'

        # FIXME: maybe this should go to __main__
        self.keyboard_index = \
            tuple(KEYBOARD_INDICES['chromatic'][direction][self.mode])

        if isinstance(tonic, list) or isinstance(tonic, tuple):
            tonic = choice(tonic)
        elif isinstance(tonic, str) and ',' in tonic:
            tonic = tonic.replace(' ', '')
            tonic = choice(tonic.split(','))
        elif isinstance(tonic, str) and ('R' in tonic or 'r' in tonic):
            tonic = choice(KEYS)

        self.tonic_pitch = Pitch(note=tonic, octave=self.octave)
        self.tonic_str = str(self.tonic_pitch.note)
        self.tonic_pitch_str = str(self.tonic_pitch)

        if not chromatic:
            self.scale = DiatonicScale(tonic=self.tonic_str, mode=mode,
                                       octave=self.octave,
                                       descending=descending,
                                       n_octaves=n_octaves)
        else:
            self.scale = ChromaticScale(tonic=self.tonic_str,
                                        octave=self.octave,
                                        descending=descending,
                                        n_octaves=n_octaves)

        self.diatonic_scale = DiatonicScale(tonic=self.tonic_str, mode=mode,
                                            octave=self.octave,
                                            descending=descending,
                                            n_octaves=n_octaves)

        self.chromatic_scale = ChromaticScale(tonic=self.tonic_str,
                                              octave=self.octave,
                                              descending=descending,
                                              n_octaves=n_octaves)

        self.allowed_pitches = \
            get_valid_pitches(self.scale, valid_intervals=valid_intervals)

        self.durations = default_durations
        if user_durations:
            ud_index = {
                0: ('preq', 'duration'),
                1: ('preq', 'delay'),
                2: ('preq', 'pos_delay'),
                3: ('quest', 'duration'),
                4: ('quest', 'delay'),
                5: ('quest', 'pos_delay'),
                6: ('resol', 'duration'),
                7: ('resol', 'delay'),
                8: ('resol', 'pos_delay'),
            }
            ud = user_durations.split(',')
            if len(ud) == len(ud_index):
                for idx, v in ud_index.items():
                    cur_duration = ud[idx].strip()
                    if cur_duration != 'n':
                        self.durations[v[0]][v[1]] = float(cur_duration)

        self.prequestion_method = prequestion_method
        self.resolution_method = resolution_method

    def make_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def make_resolution(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def play_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def check_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

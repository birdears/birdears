import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import NoTransition

from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import StringProperty, ObjectProperty

from kivy.clock import Clock

from ...sequence import Sequence

class NonblockingSequence(Sequence):

    def __init__(self, elements=[], duration=2, delay=1.5, pos_delay=1):
        super(NonblockingSequence, self).__init__(elements=elements,
                                                  duration=duration,
                                                  delay=delay,
                                                  pos_delay=pos_delay)

        self.index = 0;
        self.last_idx = len(self.elements) - 1
        self.iterator = iter(self)

    def play_callback(self, dt):
        try:
            #a = next(self.iterator)
            a = next(self)

            print(a)
            if not a['is_last']:
                Clock.schedule_once(self.play_callback, a['delay'])
        except StopIteration:
            self.iterator = iter(self)
            print('exception recvd..')


    def __iter__(self):
        return self

    def __next__(self):
        """Plays the next element of note and/or chord in the Sequence and
        schedules the next event.
        """

        is_last = True if self.index == self.last_idx else False

        #last_idx = len(self.elements) - 1

        element = self.elements[self.index]
        # for cur_idx, element in enumerate(self.elements):

        # lets leave the last element's delay for pos_delay:

        delay = self.delay if not is_last else 0

        if type(element) == tuple:
            el, duration, delay = element
        else:
            el = element

        if type(el) == str:
            self._play_note(el, delay=delay)
        elif type(el) == list:
            self._play_chord(element, delay=delay)

        self.play_element(self.index)

        current_data = dict(
            index=self.index,
            element=el,
            delay=delay,
            is_last=is_last
        )

        self.index += 1

        #yield current_data
        return current_data

    def _wait(self, seconds):
        pass

#Builder.load_file('interfaces/gui/birdears.kv')

class BirdearsScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(BirdearsScreenManager, self).__init__(**kwargs)


class InitialScreen(Screen):
    def __init__(self, **kwargs):
        super(InitialScreen, self).__init__(**kwargs)

class ExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super(ExerciseScreen, self).__init__(**kwargs)

        self.add_widget(ExerciseWidget())

class ExerciseWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(ExerciseWidget, self).__init__(**kwargs)

        valid_semitones = self.question.get_valid_semitones()

        for semitone in valid_semitones:
            bt = getattr(self, "bt{btid}".format(btid=semitone))

            bt.disabled = False
            bt.keyboard = self.question.keyboard_index[semitone]
            bt.semitone = semitone

            print(bt.keyboard)

        nbprequestion = \
            NonblockingSequence(elements=self.question.pre_question.elements,
                                duration=self.question.pre_question.duration,
                                delay=self.question.pre_question.delay,
                                pos_delay=self.question.pre_question.pos_delay)

        nbquestion = \
            NonblockingSequence(elements=self.question.question.elements,
                                duration=self.question.question.duration,
                                delay=self.question.question.delay,
                                pos_delay=self.question.question.pos_delay)

        #play_iter = iter(nbquestion)
        #nbquestion.play_next(play_iter)
        Clock.schedule_once(nbprequestion.play_callback, 0)
        Clock.schedule_once(nbquestion.play_callback, 1)

    def check_question(self, semitone):

        self.question.play_resolution()

        keyboard = self.question.keyboard_index[semitone]
        response = self.question.check_question([keyboard])

        print(response)

class BirdearsApp(App):

    def build(self):

        self.sm =  BirdearsScreenManager(transition=NoTransition())
        self.sm.switch_to(InitialScreen(name='initial'))

        return self.sm

    def show_screen(self, screen_name):
        self.sm.current = screen_name

    def show_exercise(self, exercise):

        if exercise == 'melodic':
            from ...questions.melodicinterval import MelodicIntervalQuestion
            self.question = MelodicIntervalQuestion()
        elif exercise == 'harmonic':
            from ...questions.harmonicinterval import HarmonicIntervalQuestion
            self.question = HarmonicIntervalQuestion()
        elif exercise == 'dictation':
            from ...questions.melodicdictation import MelodicDictationQuestion
            self.question = MelodicDictationQuestion()
        elif exercise == 'instrumental':
            from ...questions.instrumentaldictation import\
                InstrumentalDictationQuestion
            self.question = InstrumentalDictationQuestion()


        print(self.question)
        #self.sm.current = 'exercise'
        # self.sm.current = screen_name
        self.sm.switch_to(ExerciseScreen(name='exercise'))

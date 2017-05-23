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

        self.question.play_question()

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
            from ...questions.instrumentaldictation import InstrumentalDictationQuestion
            self.question = InstrumentalDictationQuestion()


        print(self.question)
        #self.sm.current = 'exercise'
        # self.sm.current = screen_name
        self.sm.switch_to(ExerciseScreen(name='exercise'))

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

# from kivy.uix.screenmanager import FadeTransition, NoTransition
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

    #bt11 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ExerciseWidget, self).__init__(**kwargs)
        self.bt11.disabled = True
        #for child in self.children:
        #    print(child)
        #print(self.ids.interval_buttons)
        print(self.bt11)



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


        print(self.question)
        #self.sm.current = 'exercise'
        # self.sm.current = screen_name
        self.sm.switch_to(ExerciseScreen(name='exercise'))

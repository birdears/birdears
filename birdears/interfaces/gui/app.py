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

        #self.add_widget(ExerciseWidget())

class ExerciseWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ExerciseWidget, self).__init__(**kwargs)

class BirdearsApp(App):

    def build(self):
        # return Label(text='hello, world!!')

            # BirdearsScreenManager(initial_screen=InitialScreen(),
        self.sm =  BirdearsScreenManager(transition=NoTransition())
        self.sm.add_widget(InitialScreen(name='initial'))
        self.sm.add_widget(ExerciseScreen(name='exercise'))
        self.sm.current = 'initial'

        return self.sm

    def show_screen(self, screen_name):
        self.sm.current = screen_name

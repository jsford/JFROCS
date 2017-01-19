#! /usr/bin/python
from kivy.app import App
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class WorldviewWidget(Widget):
    def __init__(self, **kwargs):
        super(WorldviewWidget, self).__init__(**kwargs)

        self.canvas.clear()
        print self.size, self.pos
        
        with self.canvas:
            Color(1, 0, 0, 1, mode='rgba')
            self.rect = Rectangle(size=???, pos=???)


class JFROCS_App(App):

    def build(self):
        Window.clearcolor = [1,1,1,1]
        parent = FloatLayout(size=Window.size)

        worldview = WorldviewWidget(size_hint=(0.4, 0.4), pos_hint = {'x':0.2, 'y':0.2})
        parent.add_widget(worldview)
        

        start_btn = Button(text='Start', size_hint=(0.1, 0.1), pos_hint={'x':.02, 'y':.7}, background_color=[0,1,0,1])
        start_btn.bind(on_release=self.start_simulation)
        parent.add_widget(start_btn)
 
        pause_btn = Button(text='Pause', size_hint=(0.1,0.1), pos_hint={'x':.02, 'y':.6}, background_color=[1,1,0,1])
        pause_btn.bind(on_release=self.pause_simulation)
        parent.add_widget(pause_btn)

        stop_btn = Button(text='Stop', size_hint=(0.1,0.1), pos_hint={'x':.02, 'y':.5}, background_color=[1,0,0,1])
        stop_btn.bind(on_release=self.stop_simulation)
        parent.add_widget(stop_btn)

        return parent

    def start_simulation(self, obj):
        print "You pushed the start button!"
    def pause_simulation(self, obj):
        print "You pushed the pause button!"
    def stop_simulation(self, obj):
        print "You pushed the stop button!"
     
if __name__ == '__main__':
    JFROCS_App().run()

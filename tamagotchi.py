from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar

class Tamagotchi(FloatLayout):
    def __init__(self, **kwargs):
        super(Tamagotchi, self).__init__(**kwargs)
        
        self.stage = "egg"
        self.points=0
        self.level=1

        self.title = Label(
                        text= "TomDuck",
                        font_size= 18,
                        color= '#000000',
                        pos_hint={"center_x": 0.5, "center_y": 0.95}
                        )
        self.add_widget(self.title)
        
        self.level_bar = Label(
                        text= f'Level {self.level}',
                        font_size= 18,
                        color= '#000000',
                        pos_hint={"center_x": 0.1, "center_y": 0.9}
                        )
        self.add_widget(self.level_bar)
        self.pb_level = ProgressBar(max=self.level*2, pos_hint={"center_x": 0.5, "center_y": 0.9}, size_hint_x=.5)
        self.pb_level.value = self.points
        self.add_widget(self.pb_level)
        self.life = Label(
                        text= "Life",
                        font_size= 18,
                        color= '#000000',
                        pos_hint={"center_x": 0.1, "center_y": 0.8}
                        )
        self.add_widget(self.life)
        pb_life = ProgressBar(max=100, pos_hint={"center_x": 0.5, "center_y": 0.8}, size_hint_x=.5)

# this will update the graphics automatically (75% done)
        pb_life.value = 50
        self.add_widget(pb_life)
        self.image = Image(source="images/egg.png",
                           size_hint=(None, None),
                           size=(125, 125),
                           pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.add_widget(self.image)
        
        self.background_color = (1, 1, 1, 1)  # set the background color to white
        
        Clock.schedule_interval(self.update, 1.0)
    
    def level_up(self):
        if self.points==self.level*2:
            self.points=0
            self.level=self.level+1
            self.pb_level.max = self.level*2
            self.pb_level.value=self.points
            self.level_bar.text = f'level {self.level}'
            print(self.level)
    
    def update(self, dt):
        if self.level == 3:
            self.image.source = "images/egg.png"
        elif self.level == 6:
            self.image.source = "images/baby.webp"
        elif self.level == 12:
            self.image.source = "images/child.png"
        elif self.level == 20:
            self.image.source = "images/adult.jpg"
    
    def on_button_press(self):
        self.points=self.points+1
        self.pb_level.value = self.points
        #print(self.points)
        self.level_up()


class TamagotchiApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return Tamagotchi()


if __name__ == "__main__":
    TamagotchiApp().run()
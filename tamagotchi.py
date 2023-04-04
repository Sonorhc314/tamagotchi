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
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import requests
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.zbarcam import ZBarCam
import serial
import car

address = '84:C6:92:B0:84:47'
baud_rate = 9600
ser = serial.Serial('COM3', baud_rate)

barcode_cache = {
    '90162602': str(int(100 - 0.63828*100)),
    '5000128943710': str(int(100 - 0.0246*100)),
    '5010018003165': str(int(100 - 0.57348*100))
}
headers = {
            "accept": "application/json",
            "authorization": "Bearer 648accfc18a23fee30bf0fdc7edd91c9"
        }

robot = car.Car()

class Scanner(BoxLayout):

    def __init__(self, tamagotchi_instance, **kwargs):
        super(Scanner, self).__init__(**kwargs)
        self.tamagotchi = tamagotchi_instance
        self.cleared = True
        self.carbon_points = 0
        Window.clearcolor = (1, 1, 1, 1)
        vbox = BoxLayout(orientation='vertical', pos_hint= {'x': 0.1, 'y': 0.5})

        self.label = Label(text="Scan a barcode", size_hint=(None, None), size=(300, 50), color=(0,0,0))
        self.label.id = 'scanner_label'
        vbox.add_widget(self.label) 
        confirm = Button(text='Confirm', size_hint=(None, None), size=(300, 50))
        confirm.bind(on_press=lambda x: self.on_confirm(self.label))
        vbox.add_widget(confirm)

        clear = Button(text='Clear', size_hint=(None, None), size=(300, 50))
        clear.bind(on_press=lambda x: self.on_clear(self.label))
        vbox.add_widget(clear)

        go_back = Button(text='Go back', size_hint=(None, None), size=(300, 50))
        go_back.bind(on_press=lambda x: self.on_go_back())
        vbox.add_widget(go_back)

        self.add_widget(vbox)
        
        self.zbarcam = ZBarCam()
        self.add_widget(self.zbarcam)
        self.zbarcam.pos_hint = {'x': 0, 'y': 0}
        self.zbarcam.bind(symbols=self.on_symbols)

    def on_confirm(self, label):
        if self.cleared:
            label.text = "No item scanned"
        else:
            label.text = "Selection confirmed"
            self.cleared = True
            if self.carbon_points > 40:
                self.tamagotchi.points += 1
                self.tamagotchi.pb_level.value = self.tamagotchi.points
                self.tamagotchi.level_up()
            else:
                self.tamagotchi.pb_life.value -= 1
        Clock.schedule_once(lambda x: self.reset_label_text(label), 1)

    def on_clear(self, label):
        if self.cleared:
            label.text = "No item scanned"
        else:
            label.text = "Selection cleared"
            self.cleared = True
        Clock.schedule_once(lambda x: self.reset_label_text(label), 1)

    def on_go_back(self):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction='left')
        app.root.current = 'tamagotchi'

    def reset_label_text(self, label):
        label.text = 'Scan a barcode'

    def on_symbols(self, instance, symbols):
        if not self.cleared: return
        if symbols:
            data = symbols[0].data
            self.label.text = get_carbon_score(self, data)
            self.cleared = False
        else:
            self.label.text = 'Scan a barcode'

def get_carbon_score(self, barcode):
    barcode = barcode.decode('utf-8')
    if barcode in barcode_cache.keys():
        carbon_score = barcode_cache[barcode]
        self.carbon_score = int(carbon_score)
        if int(carbon_score) > 40:
            return "Carbon score: " + carbon_score + "\nThis is a more carbon-friendly product"
        else:
            return "Carbon score: " + carbon_score + "\nThis is a less carbon-friendly product"
    else:
        barcode_query = f"https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key=0rythb0zy50giv4ziuou4kmot9s6p6"
        response = requests.get(barcode_query)
        if response.status_code == 200:
            brand = response.json()['products'][0]['brand']
        else:
            return f'Error: {response.status_code} - {response.text}'
        response = requests.get(f"https://api.ditchcarbon.com/v1.0/supplier?name={brand}&currency=USD", headers=headers)
        if response.status_code == 200:
            carbon_score = str(int(100-float(response.json()['ef_kg_co2eq'])*100))
            barcode_cache[barcode] = carbon_score
            self.carbon_score = int(carbon_score)
            if int(carbon_score) > 40:
                return "Carbon score: " + carbon_score + "\nThis is a more carbon-friendly product"
            else:
                return "Carbon score: " + carbon_score + "\nThis is a less carbon-friendly product"
        else:
            return f'Error: {response.status_code} - {response.text}'
        
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
        self.pb_life = ProgressBar(max=100, pos_hint={"center_x": 0.5, "center_y": 0.8}, size_hint_x=.5)

# this will update the graphics automatically (75% done)
        self.pb_life.value = 50
        self.add_widget(self.pb_life)
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

    def on_scan_press(self):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction='right')
        app.root.current = 'scanner'

    def on_find_press(self):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction='left')
        app.root.current = 'finder'

class Finder(GridLayout):
    def __init__(self, **kwargs):
        super(Finder, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.cols=3

        s = Button(text='Sugar', size=(300, 50))
        s.bind(on_press=lambda x: self.on_s())
        self.add_widget(s)

        r = Button(text='Red Bull', size=(300, 50))
        r.bind(on_press=lambda x: self.on_r())
        self.add_widget(r)

        m = Button(text='Milk', size=(300, 50))
        m.bind(on_press=lambda x: self.on_m())
        self.add_widget(m)

        go_back = Button(text='Go back', size=(300, 50))
        go_back.bind(on_press=lambda x: self.on_go_back())
        self.add_widget(go_back)
    
    def on_s(self):
        for action in robot.get_actions('S'):
            ser.write(bytes(action, 'utf-8'))
            print(action)

    def on_r(self):
        for action in robot.get_actions('R'):
            ser.write(bytes(action, 'utf-8'))
            print(action)

    def on_m(self):
        for action in robot.get_actions('M'):
            ser.write(bytes(action, 'utf-8'))
            print(action)

    def on_go_back(self):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction='right')
        app.root.current = 'tamagotchi'

class TamagotchiScreen(Screen):
    def __init__(self, **kwargs):
        super(TamagotchiScreen, self).__init__(**kwargs)
        self.tamagotchi = Tamagotchi() 
        self.add_widget(self.tamagotchi)

class ScannerScreen(Screen):
    def __init__(self, tamagotchi_instance, **kwargs):
        super(ScannerScreen, self).__init__(**kwargs)
        self.add_widget(Scanner(tamagotchi_instance=tamagotchi_instance))

class FinderScreen(Screen):
    def __init__(self, **kwargs):
        super(FinderScreen, self).__init__(**kwargs)
        self.add_widget(Finder())

class MyScreenManager(ScreenManager):
    pass

class TamagotchiApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = MyScreenManager(transition=SlideTransition(direction='right'))
        tamagotchi_screen = TamagotchiScreen(name='tamagotchi')
        scanner_screen = ScannerScreen(tamagotchi_instance=tamagotchi_screen.tamagotchi, name='scanner')
        finder_screen = FinderScreen(name='finder')
        sm.add_widget(tamagotchi_screen)
        sm.add_widget(scanner_screen)
        sm.add_widget(finder_screen)

        return sm

if __name__ == "__main__":
    TamagotchiApp().run()
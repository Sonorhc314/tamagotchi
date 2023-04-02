import kivy
import requests

kivy.require('1.11.1')  # replace with the version of kivy you have installed

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_garden.zbarcam import ZBarCam
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock

barcode_cache = {
    '90162602': str(int(100 - 0.63828*100)),
    '5000128943710': str(int(100 - 0.0246*100)),
    '5010018003165': str(int(100 - 0.57348*100))
}
headers = {
            "accept": "application/json",
            "authorization": "Bearer 648accfc18a23fee30bf0fdc7edd91c9"
        }

class ScannerLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(ScannerLayout, self).__init__(**kwargs)
        self.cleared = True
        Window.clearcolor = (1, 1, 1, 1)
        vbox = BoxLayout(orientation='vertical', pos_hint= {'x': 0.1, 'y': 0.5})

        label = Label(text="Scan a barcode", size_hint=(None, None), size=(300, 50), color=(0,0,0))
        vbox.add_widget(label) 
        confirm = Button(text='Confirm', size_hint=(None, None), size=(300, 50))
        confirm.bind(on_press=lambda x: self.on_confirm(label))
        vbox.add_widget(confirm)
        clear = Button(text='Clear', size_hint=(None, None), size=(300, 50))
        clear.bind(on_press=lambda x: self.on_clear(label))
        vbox.add_widget(clear)
        self.add_widget(vbox)
        
        # self.zbarcam = ZBarCam()
        # self.add_widget(self.zbarcam)
        # self.zbarcam.pos_hint = {'x': 0, 'y': 0}

        # self.zbarcam.bind(symbols=self.on_symbols)

    def on_confirm(self, label):
        if self.cleared:
            label.text = "No item scanned"
        else:
            label.text = "Selection confirmed"
            self.cleared = True
        Clock.schedule_once(lambda x: self.reset_label_text(label), 1)

    def on_clear(self, label):
        if self.cleared:
            label.text = "No item scanned"
        else:
            label.text = "Selection cleared"
            self.cleared = True
        Clock.schedule_once(lambda x: self.reset_label_text(label), 1)

    def reset_label_text(self, label):
        label.text = 'Scan a barcode'

    def on_symbols(self, instance, symbols):
        if not self.cleared: return
        if symbols:
            data = symbols[0].data
            self.label.text = get_carbon_score(data)
            self.cleared = False
        else:
            self.label.text = 'Scan a barcode'

def get_carbon_score(barcode):
    barcode = barcode.decode('utf-8')
    if barcode in barcode_cache.keys():
        return "Carbon score: " + barcode_cache[barcode]
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
            return "Carbon score: " + carbon_score
        else:
            return f'Error: {response.status_code} - {response.text}'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import urllib.request
import urllib.parse
import json

class WaterFinderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.place_input = TextInput(hint_text='د ځای نوم ولیکئ', size_hint=(1, 0.2))
        self.result_label = Label(text='پایله دلته ښکاره کیږي', size_hint=(1, 0.6))
        self.search_button = Button(text='پلټنه', size_hint=(1, 0.2))
        self.search_button.bind(on_press=self.search_water)

        self.layout.add_widget(self.place_input)
        self.layout.add_widget(self.search_button)
        self.layout.add_widget(self.result_label)
        return self.layout

    def fetch_json(self, url, headers=None):
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())

    def search_water(self, instance):
        place = self.place_input.text.strip()
        if not place:
            self.result_label.text = "لومړی د ځای نوم ولیکئ"
            return
        self.result_label.text = "پلټنه روانه ده..."
        try:
            q = urllib.parse.quote(place)
            url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
            data = self.fetch_json(url, headers={"User-Agent": "WaterFinderApp/1.0"})
            if not data:
                self.result_label.text = "دا ځای ونه موندل شو."
                return
            lat, lon = data[0]["lat"], data[0]["lon"]

            water_url = (
                "https://power.larc.nasa.gov/api/temporal/climatology/point"
                f"?parameters=PRECTOTCORR&community=AG&longitude={lon}&latitude={lat}&format=JSON"
            )
            wdata = self.fetch_json(water_url)
            annual = wdata["properties"]["parameter"]["PRECTOTCORR"]["ANN"]

            if annual >= 2.5:
                level = "لوړ احتمال"
            elif annual >= 1.2:
                level = "منځنی احتمال"
            else:
                level = "ټیټ احتمال"

            self.result_label.text = f"{data[0]['display_name']}\nاوسط کلنی باران: {annual} mm/ورځ\nاحتمال: {level}"
        except Exception as e:
            self.result_label.text = f"تېروتنه: {e}"

if __name__ == '__main__':
    WaterFinderApp().run()

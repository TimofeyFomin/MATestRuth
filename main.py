from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import instructions
from kivy.uix.textinput import TextInput
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first screen'))
        sm.add_widget(SecondScreen(name='second screen'))
        sm.add_widget(ThirdScreen(name='third screen'))
        sm.add_widget(FourthScreen(name='fourth screen'))
        sm.add_widget(FifthScreen(name='fifth screen'))
        return sm
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing='10px', padding='10px')
        label = Label(text=instructions.txt_instruction)
        self.textinput_name = TextInput(size_hint=(0.8, None), height='40px',
                                   pos_hint={'center_x': 0.5}, hint_text='Имя')
        self.textinput_age = TextInput(size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5},
                                  hint_text='Возраст')
        button = Button(text='Start', background_color='red',
                        size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5})
        layout.add_widget(label)
        layout.add_widget(self.textinput_name)
        layout.add_widget(self.textinput_age)
        layout.add_widget(button)
        self.add_widget(layout)
        button.on_press = self.changing_screen

    def changing_screen(self):
        age = self.textinput_age.text
        name = self.textinput_name.text
        try:
            schema = SchemaFirstScreen(age=age, name=name)
            self.manager.current = 'second screen'
        except ValidationError:
            self.textinput_age.text = ''
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing='10px', padding='10px')
        label = Label(text=instructions.txt_test1)
        self.textinput = TextInput(size_hint=(0.8, None), height='40px',
                                   pos_hint={'center_x': 0.5}, hint_text='Введите результат')
        button = Button(text='Продолжить', background_color='green',
                        size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5})

        layout.add_widget(label)
        layout.add_widget(self.textinput)
        layout.add_widget(button)
        self.add_widget(layout)
        button.on_press = self.changing_screen
    def changing_screen(self):
        try:
            schema = SchemaDimension(dimension=self.textinput.text)
            self.manager.current = 'third screen'
        except ValidationError:
            self.textinput.text = ''
class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing='10px', padding='10px')
        label = Label(text=instructions.txt_sits)
        button = Button(text='Продолжить', background_color='green',
                        size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5})
        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)
        button.on_press = self.changing_screen
    def changing_screen(self):
        self.manager.current = 'fourth screen'
class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing='10px', padding='10px')
        label = Label(text=instructions.txt_test3)
        self.textinput_res = TextInput(size_hint=(0.8, None), height='40px',
                                   pos_hint={'center_x': 0.5}, hint_text='Результат')
        self.textinput_res2 = TextInput(size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5},
                                  hint_text='Результат после отдыха')
        button = Button(text='Завершить', background_color='green',
                        size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5})
        layout.add_widget(label)
        layout.add_widget(self.textinput_res)
        layout.add_widget(self.textinput_res2)
        layout.add_widget(button)
        self.add_widget(layout)
        button.on_press = self.changing_screen
    def changing_screen(self):
        try:
            schema = SchemaDimension(dimension=self.textinput_res.text)
        except ValidationError:
            self.textinput_res.text = ''
        try:
            schema = SchemaDimension(dimension=self.textinput_res2.text)
            self.manager.current = 'fifth screen'
        except ValidationError:
            self.textinput_res2.text = ''
class FifthScreen(Screen):
    pass
class SchemaFirstScreen(BaseModel):
    age: Optional[int] = Field(..., ge=1, le=120)
class SchemaDimension(BaseModel):
    dimension: Optional[int] = Field(..., ge=1)



app = MyApp()
app.run()
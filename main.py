from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import instructions
from kivy.uix.textinput import TextInput
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import ruffier
from kivy.properties import BooleanProperty
from kivy.clock import Clock

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
            app.user_info = SchemaFirstScreen(age=age, name=name)
            self.manager.current = 'second screen'
        except ValidationError:
            self.textinput_age.text = ''
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing='10px', padding='10px')
        label = Label(text=instructions.txt_test1)
        self.textinput = TextInput(size_hint=(0.8, None), height='40px',
                                   pos_hint={'center_x': 0.5}, hint_text='Введите результат',disabled=True)
        self.button = Button(text='Нажмите, чтобы запустить таймер', background_color='green',
                        size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5})
        self.timer = Timer(15)
        self.timer.bind(is_finish=self.unlock_items)
        layout.add_widget(label)
        layout.add_widget(self.timer)
        layout.add_widget(self.textinput)
        layout.add_widget(self.button)
        self.add_widget(layout)
        self.button.on_press = self.changing_screen
    def changing_screen(self):
        if not self.timer.is_finish:
            self.button.disabled = True
            self.button.text = 'Продолжить'
            self.timer.start_timer()
        try:
            app.p1 = SchemaDimension(dimension=self.textinput.text)
            self.manager.current = 'third screen'
        except ValidationError:
            self.textinput.text = ''
    def unlock_items(self, *args):
        self.button.disabled = False
        self.textinput.disabled = False
class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing='10px', padding='10px')
        label = Label(text=instructions.txt_sits)
        self.button = Button(text='Запустить таймер', background_color='green',
                        size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5})
        self.timer = Timer(45)
        self.timer.bind(is_finish=self.unlock_button)
        layout.add_widget(label)
        layout.add_widget(self.timer)
        layout.add_widget(self.button)
        self.add_widget(layout)
        self.button.on_press = self.changing_screen
    def changing_screen(self):
        if not self.timer.is_finish:
            self.button.disabled = True
            self.timer.start_timer()
        if self.button.text == 'Продолжить':
            self.manager.current = 'fourth screen'
    def unlock_button(self, *args):
        self.button.text = 'Продолжить'
        self.button.disabled = False

class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing='10px', padding='10px')
        label = Label(text=instructions.txt_test3)
        self.textinput_res = TextInput(size_hint=(0.8, None), height='40px',
                                   pos_hint={'center_x': 0.5}, hint_text='Результат',
                                   disabled = True)
        self.textinput_res2 = TextInput(size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5},
                                  hint_text='Результат после отдыха', disabled = True)
        self.button = Button(text='Запустить таймер', background_color='green',
                        size_hint=(0.8, None), height='40px', pos_hint={'center_x': 0.5})
        self.stages = [15, 30, 15]
        self.stages_index = 0
        self.timer = Timer(self.stages[self.stages_index])
        self.timer.bind(is_finish=self.restarting_timer)
        layout.add_widget(label)
        layout.add_widget(self.timer)
        layout.add_widget(self.textinput_res)
        layout.add_widget(self.textinput_res2)
        layout.add_widget(self.button)
        self.add_widget(layout)
        self.button.on_press = self.changing_screen
    def changing_screen(self):
        if not self.timer.is_finish:
            self.button.disabled = True
            self.timer.start_timer()
        elif self.button.text == 'Завершить':
            try:
                app.p2 = SchemaDimension(dimension=self.textinput_res.text)
            except ValidationError:
                self.textinput_res.text = ''
            try:
                app.p3 = SchemaDimension(dimension=self.textinput_res2.text)
                self.manager.current = 'fifth screen'
            except ValidationError:
                self.textinput_res2.text = ''

    def restarting_timer(self, instance, value, ):
        if value is not True:
            return

        self.stages_index += 1
        if self.stages_index < len(self.stages):
            if self.stages_index == 1:
                self.textinput_res.disabled = False
            elif self.stages_index == 2:
                self.textinput_res2.disabled = False
            self.timer.is_finish = False
            self.timer.restart_timer(self.stages[self.stages_index])
        else:
            self.button.text = 'Завершить'
            self.button.disabled = False

class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text='')
        self.add_widget(self.label)
        self.on_enter = self.get_answer
    def get_answer(self):
        answer = ruffier.test(app.p1.dimension, app.p2.dimension, app.p3.dimension, app.user_info.age)
        self.label.text = answer
class SchemaFirstScreen(BaseModel):
    age: Optional[int] = Field(..., ge=1, le=120)
    name: Optional[str]
class SchemaDimension(BaseModel):
    dimension: Optional[int] = Field(..., ge=1)
class Timer(Label):
    is_finish = BooleanProperty(False)
    def __init__(self, time, **kwargs):
        self.time = time
        self.is_finish = False
        self.current = 0
        self.text = f'Прошло секунд: {self.current}'
        self.event = None
        super().__init__(text=self.text, **kwargs)
    def change_text_timer(self, dt):
        self.current += 1
        self.text = f'Прошло секунд: {self.current}'
        if self.current >= self.time:
            self.is_finish = True
            return False
    def restart_timer(self, time):
        self.is_finish = False
        self.time = time
        self.current = 0
        self.text = f'Прошло секунд: {self.current}'
        self.start_timer()
    def start_timer(self):
        Clock.schedule_interval(self.change_text_timer, 1)






app = MyApp()
app.run()
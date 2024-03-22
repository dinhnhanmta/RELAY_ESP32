# code to show how to use nested boxlayouts.
 
# import kivy module 
import kivy 
import random  
from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from functools import partial
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import re
from datetime import datetime


red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
blue =  [0, 0, 1, 1]
purple = [1, 0, 1, 1]

class My_TextInput(TextInput):
    max_length = 16
    def __init__(self, **kwargs):
        super(My_TextInput, self).__init__(**kwargs)
    def set_cursor(self, instance, text):
        self.cursor = (len(self.text), 0)

    def on_text(self, instance, text):
        if(len(text) == 2 or len(text) == 5 or len(text) == 8 or len(text) == 11 or len(text) == 14 ):
            self.text += ":"
            Clock.schedule_once(partial(self.do_cursor_movement, 'cursor_end')) 
    
    def insert_text(self, substring, from_undo = False):
        s = substring.upper().strip()
        if len(self.text) <= self.max_length:
            return super(My_TextInput, self).insert_text(s, from_undo = from_undo)
            
            
            
       
# class in which we are creating the button 
class BoxLayoutApp(App): 
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("realyesp32.json", scopes)
    client = gspread.authorize(creds)
    
    # draw function
    def build(self):
 
        superBox = BoxLayout(orientation ='vertical')
 
        # To position widgets next to each other,
        # use a horizontal BoxLayout.
        InputBox = BoxLayout(orientation ='horizontal', size_hint =(1, 0.8))
 
        colors = [red, green, blue, purple]
    
        # HB represents the horizontal boxlayout orientation
        # declared above
        self.MAC_text = My_TextInput(size_hint = (0.7,1),hint_text ='xx:xx:xx:xx:xx:xx')
        self.temp_text = TextInput(size_hint = (0.7,1), input_filter = 'float')
        inputText = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        inputText.add_widget(Button(text='MAC Adress', size_hint=(0.3,1)))
        inputText.add_widget(self.MAC_text)
        inputText.add_widget(Button(text='Temperature', size_hint=(0.3,1)))
        inputText.add_widget(self.temp_text)
        InputBox.add_widget(inputText)
        # To position widgets above/below each other,
        # use a vertical BoxLayout.
        ButtonBox = BoxLayout(orientation ='vertical', size_hint =(1, 0.2))
 
        btnSubmit = Button(text ="Three",
                      background_color = blue,
                      font_size = 32,
                      size_hint =(1, 10))
        btnSubmit.bind(on_press=self.on_button_press)
        ButtonBox.add_widget(btnSubmit)
        
        # superbox used to again align the oriented widgets
        superBox.add_widget(InputBox)
        superBox.add_widget(ButtonBox)
 
        return superBox
    def on_button_press(self, instance):
        # Retrieve text from input field
        temp_input = self.temp_text.text
        mac_input = self.MAC_text.text
        print("Text entered:", temp_input)
        sheet = self.client.open("FirstSheet").sheet1
        mac_get_from_sheet = sheet.col_values(1)
        temp_get_from_sheet = sheet.col_values(2)

        # datetime object containing current date and time
        now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
       
        #r = re.compile('.{2}:.{2}:.{2}:.{2}:.{2}:.{2}')
        #if r.match(mac_input) is not None:
        #    print ('matches')
        #else:
        #    print('Error')

        #mac_get_from_sheet.append(mac_input) if mac_input not in mac_get_from_sheet else mac_get_from_sheet
        #temp_get_from_sheet[mac_get_from_sheet.index(mac_input)] = temp_input
        #mac_col = sheet.range('A1')
        #sheet.update_cells('A1')
        data = [mac_input, temp_input,now]
        if mac_input not in mac_get_from_sheet:
            sheet.insert_row(data)
        else:
            sheet.update_cell(mac_get_from_sheet.index(mac_input)+1,2,temp_input)
            sheet.update_cell(mac_get_from_sheet.index(mac_input)+1,3,now)


# creating the object root for BoxLayoutApp() class  
root = BoxLayoutApp()  
root.run() 
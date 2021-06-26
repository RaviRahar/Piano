# Comments explain the line of code that is below them

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, NoTransition, RiseInTransition, FadeTransition

from kivymd.uix.label import MDLabel
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.gridlayout import MDGridLayout

from kivy.uix.label import Label
import webbrowser

class LinkLabel(MDLabel):
    def __init__(self, **kwargs):
        self.target=kwargs.pop('target')
        kwargs['markup']=True
        kwargs['font_size']=18
        kwargs['text']="[ref=link]{}[/ref]".format(kwargs['text'])
        kwargs['on_ref_press']=self.link
        super().__init__(**kwargs)

    def link(self, *args):
        webbrowser.open(self.target)

# to change notes' sounds, just replace their file and respective name here.
# note that no. of notes should remain same or else change their size_hint, 
# position_hint in on_enter() function in MainScreen() class
white_notes=['c4', 'd4', 'e4', 'f4', 'g4', 'a5', 'b5', 'c5']      
black_notes=['c-4', 'd-4', 'f-4', 'g-4', 'a-5']
note_volume=1

# to change/add beat here, also change/add respective button in piano.kv 
# (its in <SettingsScreen> last lines)
beats=['Beat 1', 'Beat 2', 'Beat 3', 'Beat 4', 'Beat 5']
beat_volume=.3
# also the default beat index
active_beat_index=0

class ScreenManagement(ScreenManager):

    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        # the esc key
        if key==27:                                                                       
            if self.current_screen.name=='main':
                # exit the app from this page
                return False                                                                
            elif self.current_screen.name=='settings':
                individual_settings=self.get_screen('settings').ids.individual_settings
                if individual_settings.my_y_hint>0:
                    self.get_screen('settings').individual_settings_card_state('down')
                    # do not exit the app
                    return True                                                             
                else:
                    self.current='main'
                    # do not exit the app
                    return True                                                             
            elif self.current_screen.name=='about':
                self.current='settings'
                return True

class SettingsScreen(MDScreen): 
    # required to change the text of active beat in active beat label
    active_beat=StringProperty(beats[active_beat_index])                

    beats_loaded=[]
    for _itr in range(len(beats)):
        beats_loaded.append(SoundLoader.load(f'media/beats/{beats[_itr]}.wav'))
    
    # controls widgit's state(disable/opaque) as per position of card
    def individual_settings_card_state(self, direction):                                             
        # hide card if partially visible else hide it
        if direction=='up':                                                               
            anim=Animation(my_y_hint=.9, t='out_quint')                                             
            anim.start(self.ids.individual_settings)
            # disable and hide all buttons and switches on settings screen
            for child in reversed(self.ids.float_settings.children):                        
                if isinstance(child, MDStackLayout) or isinstance(child, MDSwitch):
                    child.disabled=1
                    child.opacity=0 if child.disabled else 1

        elif direction=='down':
            anim=Animation(my_y_hint=0, t='out_quint')
            anim.start(self.ids.individual_settings)
            # enable and show all buttons and switches on settings screen
            for child in reversed(self.ids.float_settings.children):                         
                if isinstance(child, MDStackLayout) or isinstance(child, MDSwitch):
                    child.disabled=0
                    child.opacity=0 if child.disabled else 1

    def theme_switch(self, app, *args):
        if self.ids.themeswitch.active==False:
            app.theme_cls.theme_style='Light'
        else:
            app.theme_cls.theme_style='Dark'

    def beat_switch(self, *args):
        sound=self.beats_loaded[active_beat_index]
        if self.ids.beatswitch.active==True:
            if sound:
                self.stop_all_beats()
                sound.volume=beat_volume
                sound.loop=True
                sound.play()
        else:
            self.stop_all_beats()

    def change_beat(self, widget):
        global active_beat_index
        active_beat_index=beats.index(widget.text)
        self.active_beat=widget.text
        self.beat_switch()
        
    def stop_all_beats(self):
        for beat in self.beats_loaded:
            if beat.state=='play':
                beat.stop()

class MainScreen(MDScreen):
    notes_loaded=[]
    for _itr in range(len(white_notes)):
        notes_loaded.append(SoundLoader.load(f'media/notes/{white_notes[_itr]}.wav'))
    for _itr in range(len(black_notes)):
        notes_loaded.append(SoundLoader.load(f'media/notes/{black_notes[_itr]}.wav'))
     
    def on_pre_enter(self, *args): 
        # White Keys' layout start here
        for note in white_notes:
            NoteButton=Factory.CustomMDFlatButton(size_hint=(1,.125))
            self.ids[note]=NoteButton
            NoteButton.name=note
            NoteButton.bind(on_press=self.play_note)
            self.ids.white_notes_layout.add_widget(NoteButton)
            Separator=Factory.MDSeparator(height='1dp')
            if note!=white_notes[len(white_notes)-1]:
                self.ids.white_notes_layout.add_widget(Separator)
        # Black Keys' layout starts here
        count=1
        top_position=1
        note_index=0
        while note_index<len(black_notes):
            note=black_notes[note_index]
            if count!=3:
                top_position-=.08
                NoteButton=Factory.MDRaisedButton(size_hint=(.65,.09), pos_hint={'right':1, 'top':top_position})
                NoteButton.md_bg_color=(0,0,0,1)
                NoteButton.name=note
                self.ids.black_notes_layout.add_widget(NoteButton)
                NoteButton.bind(on_press=self.play_note)
                top_position-=.045
                count+=1
                note_index+=1
            else:
                top_position-=.08
                top_position-=.045
                count=0

    def on_leave(self, *args):
        self.ids.white_notes_layout.clear_widgets()
        self.ids.black_notes_layout.clear_widgets()

    def play_note(self, button, *args):
        if self.ids.speed_dial_stack.state=='open':
            self.close_speed_dial_stack()
        note=button.name
        if note in black_notes:
            note=self.notes_loaded[black_notes.index(note)+len(white_notes)]
        elif note in white_notes:
            note=self.notes_loaded[white_notes.index(note)]
        if note:
            note.volume=note_volume
            note.play()

    def speed_dial_call(self, button):
        if button.icon=='music-circle-outline':
            self.toggle_switch('beatswitch')
        elif button.icon=='theme-light-dark':
            self.toggle_switch('themeswitch')
        elif button.icon=='cog-outline':
            self.manager.transition=RiseInTransition()
            self.manager.transition.duration=0.1
            self.manager.current='settings'
            self.manager.transition=FadeTransition()
        self.close_speed_dial_stack()

    def close_speed_dial_stack(self):
        self.ids.speed_dial_stack.close_stack()
    def toggle_switch(self, switch):
        switch=self.parent.get_screen('settings').ids[switch]
        if switch.active==True:
            switch.active=False
        else:
            switch.active=True
            
class AboutScreen(MDScreen):
    def on_pre_enter(self, *args):
        HeadingLabel=Factory.MDLabel(text='About', halign='left', padding=(10,5))
        NameLabel=Factory.MDLabel(text='Ravi', halign='center')
        GithubLink=Factory.LinkLabel(text='Show Github', target='https://github.com/RaviRahar', halign='center')
        AppGithubLink=Factory.LinkLabel(text='Source Code', target='https://github.com/RaviRahar/Piano', halign='center')
        DesclaimerLabel=Factory.MDLabel(text='Disclaimer', halign='center', size_hint=(1,0.2))
        DesclaimerStatementLabel=Factory.MDLabel(halign='left', size_hint=(1,0.6), padding=(10,5))
        DesclaimerStatementLabel.text='All rights for author of each beat remain with them. ALL beats are taken from FMA(Free Music Archieve). None is used here for commercial purpose'
        VersionLabel=Factory.MDLabel(text='[size=30]Version 0.1[/size]', markup=True, halign='center')
        self.ids.about_developer.add_widget(HeadingLabel)
        self.ids.about_developer.add_widget(NameLabel)
        self.ids.about_developer.add_widget(GithubLink)
        self.ids.about_developer.add_widget(AppGithubLink)
        self.ids.about_app.add_widget(DesclaimerLabel)
        self.ids.about_app.add_widget(DesclaimerStatementLabel)
        self.ids.about_app.add_widget(VersionLabel)
        
    def on_leave(self, *args):
        self.ids.about_developer.clear_widgets()
        self.ids.about_app.clear_widgets()

class CustomMDFlatButton(MDFlatButton):
    def on_touch_down(self, touch, *arg):
        black_button_touched=False
        for child in self.parent.parent.parent.ids.black_notes_layout.children:
            if child.collide_point(*touch.pos):
                black_button_touched=True
        if not black_button_touched:
                return super(CustomMDFlatButton, self).on_touch_down(touch)
        else:
            pass
 
# DummyScreen is added because on_pre_enter in MainScreen is unable to
# access ids because they were not created so early
class DummyScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.switch_screen)

    def switch_screen(self, dt):
        self.manager.transition=NoTransition()
        self.manager.current="main"
        self.manager.transition=FadeTransition()

class PianoApp(MDApp):
    def build(self):
        return

if (__name__=='__main__'):
    PianoApp().run()

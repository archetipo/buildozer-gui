#!/usr/bin/python
#-*- coding:utf-8 -*-
from kivy.uix.gridlayout import GridLayout
from kivy.properties import (NumericProperty, StringProperty,
                            BooleanProperty, ObjectProperty, DictProperty,
                            AliasProperty, ListProperty)
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout

Builder.load_string('''
<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)

<SaveDialog>:
    text_input: text_input
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            on_selection: text_input.text = self.selection and self.selection[0] or ''

        TextInput:
            id: text_input
            size_hint_y: None
            height: 30
            multiline: False

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Save"
                on_release: root.save(filechooser.path, text_input.text)


<InfoBubble>:
    size_hint: None, None
    width:
        min(txt._label_cached.get_extents(self.info)[0], 360)\
        if txt._label_cached else 360
    height: min(txt.height + 5, Window.height)
    BoxLayout:
        padding: 2
        ScrollView:
            id:scrl
            TextInput:
                id: txt
                background_color: .1188, .1188, .1188, .1
                foreground_color: .8811, .8811, .8811, .5544
                size_hint: 1, None
                text: root.info
                height:
                    (len(self._lines)+1) *\
                    ((self.line_height))

<LabelInput>:
    size_hint: 1, None
    height: '30dp'
    rows: 1
    overlay_text: 'Sample Value'
    label: 'Empty'
    help_msg: 'Help Msg!!'
    arrow_pos: 'left_mid'
    input_type: 'text'
    text: txt.text
    Label:
        text: root.label
        size_hint: None, 1
        font_size: '13.5sp'
        width: '120dp'
    TextInput:
        id: txt
        border: 4, 4, 4, 4
        background_color: .8811, .8811, .8811, .8811
        on_text:
            # args[1] is the text value
            value = args[1]
            if value == root.overlay_text:\\
            self.cursor = (0, 0); self.text = '';\\
            self._trigger_refresh_text();\\
            value = ''
            op = 1
            if value != '': op = 0
            Animation(opacity=op, d=1).start(lbl)
        on_focus:
            if args[1]: root.show_info_bubble(root.help_msg);\\
            root.show_options(self)
    Button:
        id: btn_hlp
        size_hint: None, 1
        width: self.height
        text: '?'
        on_release: root.show_info_bubble(root.help_msg)
    FloatLayout:
        size_hint: None, None
        size: 0,0
        Label:
            id:lbl
            color: .5, .5, .5, 1
            text: root.overlay_text
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            pos: txt.pos
            size_hint: None, None
            size: txt.size

<PopupWarning>:
    title: 'Hide Your Cats!!!'
    auto_dismiss: False
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: '[color=ff0000][b]Warning: all uncommited changes will be'+\
            ' deleted[/b][/color]\\nAre You sure you want to run' +\
            ' "[color=00ff00][b]git clean -dxf[/b][/color]" ?'
            markup: True
        BoxLayout:
            size_hint: 1, .1
            Button:
                text: 'Ok, Cats Are Hidden'
                on_release:
                    root.do_command = True
                    root.dismiss()
            Button:
                text: 'Cancel'
                on_release:
                    root.do_command = False
                    root.dismiss()
''')
class InfoBubble(Bubble):

    info = StringProperty('Help Msg!!')
    '''This holds the Text to be displyed in the Bubble
    '''

    duration = NumericProperty(2)
    '''Signifies how long the info will be displayed for

    `:data:duration` is a `:class:~/kivy.properties.NumericProperty` defaults
    to 3
    '''

    def show(self, pos=(0,0), info='Help Msg!!'):
        win = Window
        self.opacity = 0
        self.info = info
        win.add_widget(self)
        anim = (Animation(opacity=1, x=pos[0], center_y=pos[1], d=.5) +
                Animation(opacity=1, d=self.duration) +
                Animation(opacity=0, d=1))
        anim.bind(on_complete=self.anim_complete)
        Clock.schedule_once(lambda dt:anim.start(self))

    def anim_complete(self, *args):
        Window.remove_widget(self)


class LabelInput(GridLayout):

    def show_info_bubble(self, info):
        if not hasattr(Window, 'info_bubble'):
            Window.info_bubble = InfoBubble()
            Window.info_bubble.limit_to = Window
        info_bubb = Window.info_bubble
        info_bubb.arrow_pos = self.arrow_pos
        info_bubb.show(pos=(self.right, self.center_y),
                        info=info)

    def defocus(self, txt_inp, *args):
        txt_inp.focus = False

    def dropdown_select(self, drpdn, txt, btn, touch):
        if btn.collide_point(*touch.pos):
            txt.text = btn.text
            drpdn.select(btn.text)

    def show_options(self, txt_inp):
        input_type = self.input_type

        if self.input_type == 'bool':
            txt_inp.readonly = True
            txt = (self.overlay_text
                    if txt_inp.text == '' else
                    txt_inp.text)
            txt_inp.text = 'False' if txt[0] == 'T' else 'True'
            Clock.schedule_once(lambda dt:self.defocus(txt_inp))

        elif input_type.startswith('options'):
            _options = input_type.split(':')[1:]
            txt_inp.readonly = True
            drpdn = DropDown()
            for opt in _options:
                drpdn.add_widget(
                    Button(text=opt,
                            background_color=(0, 0, 0, 1),
                            on_touch_up=partial(self.dropdown_select,
                                                drpdn, txt_inp),
                        size_hint_y=None, height = '36sp'))
            drpdn.open(txt_inp)
            Clock.schedule_once(lambda dt: self.defocus(txt_inp))


class PopupWarning(Popup):
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from win32api import GetSystemMetrics
from kivy.config import Config
from kivy.uix.textinput import TextInput

import src.Game as G
import src.Board as B


class BoardGrid(GridLayout):
    def __init__(self, **kwargs):
        self.mode = kwargs.pop('mode')
        super(BoardGrid, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        self.fill_grid()

    def fill_grid(self):
        board = g.player1.board
        col = board.columns[:10]
        row = board.index

        if self.mode == 'player':
            board_list = board.iloc[:,:10].stack().tolist()
        if self.mode == 'opponent':
            board_list = board.iloc[:,12:].stack().tolist()
        print(self.mode)
        for i in board_list:
            self.btn = ToggleButton(text=str(i))
            self.add_widget(self.btn)
            self.btn.bind(on_press=self.pressed)


    def pressed(self,instance):
        winner = g.goRound()


class WindowGrid(GridLayout):
    def __init__(self):
        super(WindowGrid, self).__init__()
        #Window.size = (GetSystemMetrics(0),GetSystemMetrics(1))
        Window.size = (960,600)
        self.cols = 3
        self.rows = 3


        self.add_widget(Label(text='Your ships'))
        self.add_widget(Label(text=str(Window.size)))
        self.add_widget(Label(text='Opponent ships'))
        self.add_widget(BoardGrid(mode='player'))
        self.add_widget(Label(text=''))
        self.add_widget(BoardGrid(mode='opponent'))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))



class ShipsApp(App):
    def build(self):
        return WindowGrid()

if __name__ == "__main__":
    b1 = B.Board('Computer 1')
    b2 = B.Board('Computer 2')
    g = G.Game(b1, b2)
    ShipsApp().run()

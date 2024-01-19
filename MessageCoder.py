if __name__ == '__main__':
    from kivy.config import Config
    import random
    import os

    Config.set('graphics', 'resizable', '0')
    Config.set("kivy", "window_icon", "3591206.png")
    import time
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
    import kivy.core.clipboard as clipboard
    from kivy.lang import Builder
    from coder import Coder

    kv = '''
    <MenuScreen>:
    GridLayout:
        spacing: '10dp'
        cols: 1
        size_hint: (0.98, 0.97)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        Button:
            id: encode
            on_release: app.goToEncode()
        Button:
            id: decode
            on_release: app.goToDecode()
        Button:
            id: quit
            on_release: app.goToQuit()
    
    <EncodeScreen>:
    GridLayout:
        spacing: '10dp'
        cols: 1
        size_hint: (0.98, 0.97)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        Label:
            id: explanation
            halign: 'center'
            valign: 'middle'
        TextInput:
            id: code
            multiline: True
            on_text: root.not_copied()
            padding_x: [self.center[0] - self._get_text_width(max(self._lines, key=len), self.tab_width, self._label_cached) / 2.0,0] if self.text else [self.center[0], 0]
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        Button:
            id: copi
            on_release: root.copied()
        Button:
            id: toMenu
            on_release: app.goToMenu()
    
    <DecodeScreen>:
    GridLayout:
        spacing: '10dp'
        cols: 1
        size_hint: (0.98, 0.97)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        Label:
            id: explanation
            halign: 'center'
            valign: 'middle'
        Button:
            id: show_btn
            on_release: root.show()
        Label:
            id: show
            halign: 'center'
            valign: 'middle'
        Button:
            id: toMenu
            on_release: app.goToMenu()        
    
    
    <QuittingScreen>:
    GridLayout:
        spacing: '10dp'
        cols: 1
        size_hint: (0.98, 0.97)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        Button:
            id: quittin
    '''


    class MenuScreen(Screen):
        def on_pre_enter(self, *args):
            self.ids.encode.text = "Encode Message"
            self.ids.decode.text = "Decode Message"
            self.ids.quit.text = "Quit"


    class EncodeScreen(Screen):
        def on_pre_enter(self):
            self.ids.explanation.text = "Write message and press copy button to get encoded version"
            self.ids.copi.text = "Copy coded message"
            self.ids.copi.background_color = (1, 1, 1, 1)
            self.ids.toMenu.text = "Go to Menu"
            self.ids.code.text = ""

        def copied(self):
            success, tmp = self.__encode()
            if success:
                clipboard.Clipboard.copy(tmp)
                self.ids.copi.background_color = (0, 1, 0, 1)
                self.ids.copi.text = "Copied"
            else:
                self.ids.copi.background_color = (1, 0, 0, 1)
                self.ids.copi.text = tmp

        def not_copied(self):
            self.ids.copi.background_color = (1, 1, 1, 1)
            self.ids.copi.text = "Copy coded message"

        def __encode(self):
            decimalValues = []
            highest = 0
            for i in range(len(self.ids.code.text)):
                a = self.ids.code.text[i]
                if a == "ẞ":
                    a = "ß"
                tmp = ord(a)
                if tmp > highest:
                    highest = tmp
                decimalValues.append(tmp)
            coder = random.randint(int((8099 - highest) / 4), 8099 - highest)
            msg = self.__dec_to_rev_90(coder)
            for i in decimalValues:
                tmp = self.__dec_to_rev_90(i + coder)
                if tmp is None:
                    return [False, f"Failed to encode {self.ids.code.text[i]}"]
                msg += tmp
            return [True, str(msg)]

        @staticmethod
        def __dec_to_rev_90(decimal):
            if decimal > 8099 or decimal < 0:
                return None
            baseNinety = Coder.get_string(decimal)
            if len(baseNinety) < 2:
                baseNinety = "0" + baseNinety
            elif len(baseNinety) > 2:
                raise ValueError
            base90encoded = []
            for i in baseNinety:
                base90encoded.append(i)
            base90encoded.reverse()
            baseNinety = ""
            for i in base90encoded:
                baseNinety += i
            return baseNinety


    class DecodeScreen(Screen):
        def on_pre_enter(self):
            self.ids.explanation.text = "Decode message"
            self.ids.show_btn.text = "Paste coded message"
            self.ids.toMenu.text = "Go to Menu"
            self.ids.show.text = ""
            self.ids.show.background_color = (1, 1, 1, 1)

        def show(self):
            try:
                decoded = self.__decode()
            except:
                decoded = "Something went terribly wrong"
            if decoded[0]:
                words = decoded[1].split(" ")
                line = ""
                lines = []
                line_len = 0
                for word in words:
                    if len(word) >= 70:
                        line += " " + word[:70 - line_len]
                        lines.append(line)
                        line = word[70 - line_len:]
                    elif line_len + len(word) >= 70:
                        lines.append(line)
                        line_len = len(word)
                        line = word
                    else:
                        line_len += len(word) + 1
                        line += " " + word
                if line != "":
                    lines.append(line)
                text = "\n"
                for line in lines:
                    text += line + "\n"
                self.ids.show.text = text
                self.ids.show.background_color = (0, 1, 0, 1)
            else:
                self.ids.show.text = decoded[1]
                self.ids.show.background_color = (1, 0, 0, 1)

        def __decode(self):
            code = clipboard.Clipboard.paste()
            code_chars = []
            chars = []
            for i in code:
                code_chars.append(i)
            code_char_number = int(len(code_chars) / 2)
            for i in range(code_char_number):
                temp = str(code_chars.pop(0))
                temp += str(code_chars.pop(0))
                chars.append(str(temp))
            message = ""
            coder = self.__rev_90_to_dec(chars.pop(0))
            if coder is None:
                return [False, "Can't decode - This message is corrupted"]
            for i in chars:
                tmp = self.__rev_90_to_dec(i)
                if tmp is None:
                    return [False, "Can't decode - This message is corrupted"]
                message += chr(int(tmp - coder))
            return [True, message]

        @staticmethod
        def __rev_90_to_dec(baseNinety):
            base90encoded = []
            for i in baseNinety:
                base90encoded.append(i)
            base90encoded.reverse()
            baseNinety = ""
            for i in base90encoded:
                baseNinety += i
            try:
                return Coder.get_number(baseNinety)
            except ValueError:
                return None


    class QuittingScreen(Screen):
        def on_pre_enter(self, *args):
            self.ids.quittin.background_color = "black"
            self.ids.quittin.text = f"Goodbye {os.getlogin()}"

        def on_enter(self, *args):
            time.sleep(3)
            App.get_running_app().stop()
            Window.close()


    class MessageCoder(App):

        def build(self):
            Builder.load_string(kv)
            # Window.size = (600, 400)
            self.sm = ScreenManager(transition=SwapTransition())
            self.sm.add_widget(MenuScreen(name='menu'))
            self.sm.add_widget(EncodeScreen(name='encoder'))
            self.sm.add_widget(DecodeScreen(name='decode'))
            self.sm.add_widget(QuittingScreen(name='quitting'))
            self.screens = self.sm.screens.copy()
            return self.sm

        def goToMenu(self):
            self.sm.switch_to(screen=self.screens[0])

        def goToEncode(self):
            self.sm.switch_to(screen=self.screens[1])

        def goToDecode(self):
            self.sm.switch_to(screen=self.screens[2])

        def goToQuit(self):
            self.sm.switch_to(screen=self.screens[3])


    MessageCoder().run()

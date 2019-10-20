from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout


Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
       
''')
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.viewclass = 'Label'
        self.data = [{'text': str(x)} for x in range(100)]
        # self.add_widget(RecycleBoxLayout(default_size=height=1,id='layout',default_size_hint=(1,None),size_hint_y=None,orientation='vertical'))



class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()
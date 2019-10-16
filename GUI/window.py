
######################################################################## 

# import kivy module 
import kivy 
	
# base Class of your App inherits from the App class. 
# app:always refers to the instance of your application 
from kivy.app import App 

# this restrict the kivy version i.e 
# below this kivy version you cannot 
# use the app or software 
kivy.require('1.9.0') 

# creates the button in kivy 
# if not imported shows the error 
from kivy.uix.button import Button 
	
# BoxLayout arranges children in a vertical or horizontal box. 
# or help to put the childrens at the desired location. 
from kivy.uix.boxlayout import BoxLayout 

# The GridLayout arranges children in a matrix. 
# It takes the available space and 
# divides it into columns and rows, 
# then adds widgets to the resulting “cells”. 
from kivy.uix.gridlayout import GridLayout 

# The PageLayout class is used to create 
# a simple multi-page layout, 
# in a way that allows easy flipping from 
# one page to another using borders. 
from kivy.uix.pagelayout import PageLayout 
from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '650')
Config.set('graphics', 'resizable', False)


######################################################################## 

# creating the root widget used in .kv file 
class Window(PageLayout): 
	pass

######################################################################## 

# creating the App class in which name 
#.kv file is to be named PageLayout.kv 
class WindowApp(App): 
	# defining build() 
	def build(self): 
		# returning the instance of root class 
		return Window() 

######################################################################## 
	
# creating object of Multiple_LayoutApp() class 


# run the class 




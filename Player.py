from tkinter import *	
from SetColor import *

class Player(object):
	"""droottring for Player"""
	def __init__(self, root,name,UP,DP):
		super(Player, self).__init__()
		self.UP = UP
		self.DP = DP
		self.root = root
		self.name = name
		self.frame = LabelFrame(self.root,text = self.name,foreground = 'blue')
		self.frame.pack(fill='x',padx=10,pady=8)

		self.CheckVar = IntVar()
		self.C1 = Checkbutton(self.frame, variable = self.CheckVar,onvalue = 1, offvalue = 0).pack(side = LEFT)
		#self.connected = Label(self.frame, text = self.name + ' 已連線').pack(side = LEFT)
		self.SetColorB=Button(self.frame,text="Set color",command=self.popup).pack(side = LEFT)

		self.value_B = -1
		self.value_G = -1
		self.value_R = -1
		self.rgb_text = StringVar()
		self.rgb_text.set('B:'+str(self.value_B)+ ' G:'+str(self.value_G) + ' R:'+str(self.value_R))
		self.RGB = Label(self.frame,textvariable = self.rgb_text).pack(side = RIGHT)

		self.Refresh = Button(self.frame,text="Refresh",command=self.entryValue).pack(side = LEFT)


	def delete(self):
		self.frame.destroy()

	def popup(self):
		self.x=popupWindow(self.root)
		self.root.wait_window(self.x.top)
		

	def entryValue(self):
		self.value_B = self.x.value_B
		self.value_G = self.x.value_G
		self.value_R = self.x.value_R
		self.rgb_text.set('B:'+str(self.value_B)+ ' G:'+str(self.value_G) + ' R:'+str(self.value_R))
	



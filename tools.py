from tkinter import *


def root_in_center(width=200, height=100):
	root = Tk()
	x = root.winfo_screenwidth() // 2 - width // 2
	y = root.winfo_screenheight() // 2 - height // 2
	root.geometry(f'{width}x{height}+{x}+{y}')
	return root


class SearchEntry(Entry):
	"""
	Entry field has search features like 'google search field'
	Typed text compares with strings in searchlist and listbox shows fit strings
	you can choose by row buttons or left mouse button
	"""
	def __init__(self, master=None, searchlist=None, maxvis=5, **configs):
		"""
		:param searchlist: list of strings where we search
		:param maxvis: maximum number of fit options that will be shown
		"""
		super().__init__(master, **configs)
		self.lst = Listbox(width=self['width'])
		self.max_visible = maxvis
		self.search_list = searchlist
		self.bind('<KeyRelease>', self.drop_list)
		self.bind('<Down>', self.go_down)

	def redo_list(self):
		self.lst.destroy()
		self.lst = Listbox(width=self['width'])
		self.lst.bind('<Up>', self.go_up)
		self.lst.bind('<Return>', self.select)
		self.lst.bind('<Double-ButtonRelease-1>', self.select)

	def drop_list(self, event):
		self.redo_list()
		ent = self.get().capitalize()
		iteration = 0
		for i in self.search_list:
			if re.findall(ent, i) and iteration < self.max_visible:
				iteration += 1
				self.lst.insert(END, i)
		self.show_list()

	def show_list(self):
		if self.lst.size() > 0 and self.get():
			self.lst.config(height=self.lst.size())
			self.lst.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

	def go_down(self, event):
		self.lst.focus_set()
		self.lst.activate(0)

	def go_up(self, event):
		try:
			if self.lst.curselection()[0] == 0:
				self.focus_set()
		except IndexError:
			pass

	def select(self, event):
		self.delete(0, END)
		self.insert(0, self.lst.get(ACTIVE))
		self.focus_set()
		self.drop_list(None)


if __name__ == '__main__':
	root = root_in_center()
	se = SearchEntry(root, ['1111', '11', '1234', '12315435'])
	se.pack()
	Label(root, text='agsdgas').pack()
	Label(root, text='agasdgasdga\nasdgasdga').pack()
	Label(root, text='agsdgas').pack()

	root.mainloop()

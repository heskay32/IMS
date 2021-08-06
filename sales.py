from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
import tempfile
class salesClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+130")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | Inventory Management System |   Developed By Olasunkanmi")
		self.root.config(bg="white")
		self.root.focus_force()
		#==============================================================================
		self.var_receipt=StringVar()
		self.bill_list=[]
		self.chk_print=0

		#==title===
		lbl_title=Label(self.root, text="View Customer Bills", font=("goudy old style", 30), bg="#4b100a", fg="white", bd=1, relief=RIDGE)
		lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

		lbl_receipt=Label(self.root, text="Receipt No.", font=("times new roman", 15), bg="white")
		lbl_receipt.place(x=50, y=100)

		txt_receipt=Entry(self.root, textvariable=self.var_receipt, font=("times new roman", 15), bg="lightyellow")
		txt_receipt.place(x=160, y=100, width=180, height=28)

		btn_search=Button(self.root, command=self.search, text="Search", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2")
		btn_search.place(x=355, y=100, width=120, height=28)

		btn_clear=Button(self.root, command=self.clear, text="Clear", font=("times new roman", 15, "bold"), bg="lightgray", fg="black", cursor="hand2")
		btn_clear.place(x=482, y=100, width=120, height=28)

		btn_print=Button(self.root, command=self.print, text="Print", font=("times new roman", 15, "bold"), bg="blue", fg="white", cursor="hand2")
		btn_print.place(x=610, y=100, width=80, height=28)	

		#=====Sales Frame/ Bill list======
		sales_Frame=Frame(self.root, bd=3, relief=RIDGE)
		sales_Frame.place(x=50, y=140, width=200, height=330)

		scrolly=Scrollbar(sales_Frame, orient=VERTICAL)
		self.Sales_List=Listbox(sales_Frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
		scrolly.pack(side=RIGHT, fill=Y)
		scrolly.config(command=self.Sales_List.yview)
		self.Sales_List.pack(fill=BOTH, expand=1)

		#==Bill Area=====
		bill_Frame=Frame(self.root, bd=3, relief=RIDGE)
		bill_Frame.place(x=280, y=140, width=410, height=330)

		lbl_title2=Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 20), bg="coral")
		lbl_title2.pack(side=TOP, fill=X)

		scrolly2=Scrollbar(bill_Frame, orient=VERTICAL)
		self.bill_area=Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
		scrolly2.pack(side=RIGHT, fill=Y)
		scrolly2.config(command=self.bill_area.yview)
		self.bill_area.pack(fill=BOTH, expand=1)
		self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

		#===Image=====
		self.bill_image=Image.open("images/resize2.png")
		self.bill_image=self.bill_image.resize((388,372), Image.ANTIALIAS)
		self.bill_image=ImageTk.PhotoImage(self.bill_image)

		#==Image Label=====
		lbl_image=Label(self.root, image=self.bill_image, bd=0)
		lbl_image.place(x=700, y=100)

		self.show()
#====================================================
	def show(self):
		del self.bill_list[:]  #firsr of all delete whats in the list
		self.Sales_List.delete(0,END)
		for i in os.listdir('bill'):  #for each file in the folder bill
			if i.split('.')[-1]=='txt': #for each file, split their name by '.', if the last element[-1] is txt
				self.Sales_List.insert(END,i) #insert it in the listBox
				self.bill_list.append(i.split('.')[0]) #put each txtfile in the list variable

	def get_data(self,ev):
		row=self.Sales_List.curselection()
		file_name=self.Sales_List.get(row)
		self.bill_area.delete('1.0',END)
		fp=open(f'bill/{file_name}', 'r')
		#print(fp)
		for i in fp:
			self.bill_area.insert(END,i)
		fp.close()
		self.checkprint()

	def search(self):
		if self.var_receipt.get()=="":
			messagebox.showerror("Error", "Receipt No required", parent=self.root)
		else:
			if self.var_receipt.get() in self.bill_list:
				fp=open(f'bill/{self.var_receipt.get()}.txt', 'r')
				self.bill_area.delete('1.0',END)
				for i in fp:
					self.bill_area.insert(END,i)
				fp.close()
			else:
				messagebox.showerror("Error", "Invalid Receipt No", parent=self.root)

	def clear(self):
		self.show()
		self.bill_area.delete('1.0',END)
		self.chk_print=0

	def checkprint(self):
		self.chk_print=1
			
	def print(self):

		if self.chk_print==1:
			messagebox.showinfo("Print", "Please Wait... receipt Printing", parent=self.root)
			new_file=tempfile.mktemp('.txt')
			open(new_file,'w').write(self.bill_area.get('1.0', END))
			os.startfile(new_file,'print')

		else:
			messagebox.showerror("Print", "Please Click on Bill", parent=self.root)


if __name__=="__main__":
	root=Tk()
	obj=salesClass(root)
	root.mainloop()

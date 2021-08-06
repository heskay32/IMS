from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class creditClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+130")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | Inventory Management System |   Developed By Olasunkanmi")
		self.root.config(bg="white")
		self.root.focus_force()
		#==============================================================================
		self.var_searchby=StringVar()
		self.var_searchtxt=StringVar()



		self.var_name=StringVar()
		self.var_product=StringVar()
		self.var_qty=StringVar()
		self.var_price=StringVar()
		self.var_total=StringVar()
		self.var_paydate=StringVar()

		#===search area=========
		lbl_search=Label(self.root, text="Name", bg="white", font=("goudy old style", 15))
		lbl_search.place(x=680, y=90)
	

		txt_search=Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
		txt_search.place(x=735, y=90, width=150)

		btn_search=Button(self.root, command=self.search, text="Search", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#4caf50")
		btn_search.place(x=920, y=89, width=100, height=27)


		#====title=========================
		title=Label(self.root, text="Manage Credits", font=("goudy old style", 23, "bold"), bg="#4b100a", fg="white")
		title.place(x=50, y=10, width=1000, height=50)

		#1st row==
		lbl_name=Label(self.root, text="Name", font=("goudy old style", 15), bg="white")
		lbl_name.place(x=50, y=90)

		txt_name=Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
		txt_name.place(x=150, y=90, width=180)

		#2nd row==
		lbl_product=Label(self.root, text="Product", font=("goudy old style", 15), bg="white")
		lbl_product.place(x=50, y=135)

		txt_product=Entry(self.root, textvariable=self.var_product, font=("goudy old style", 15), bg="lightyellow")
		txt_product.place(x=150, y=135, width=180)

		#3rd row==
		lbl_qty=Label(self.root, text="Qty", font=("goudy old style", 15), bg="white")
		lbl_qty.place(x=50, y=180)

		txt_qty=Entry(self.root, textvariable=self.var_qty, font=("goudy old style", 15), bg="lightyellow")
		txt_qty.place(x=150, y=180, width=100)

		#4th row==
		lbl_price=Label(self.root, text="Price", font=("goudy old style", 15), bg="white")
		lbl_price.place(x=50, y=225)

		txt_price=Entry(self.root, textvariable=self.var_price, font=("goudy old style", 15), bg="lightyellow")
		txt_price.place(x=150, y=225, width=180)

		#5th row==
		lbl_total=Label(self.root, text="Total", font=("goudy old style", 15), bg="white")
		lbl_total.place(x=50, y=270)

		txt_total=Entry(self.root, textvariable=self.var_total, font=("goudy old style", 15), bg="lightyellow")
		txt_total.place(x=150, y=270, width=180)

		#6th row==
		lbl_paydate=Label(self.root, text="Pay Date", font=("goudy old style", 15), bg="white")
		lbl_paydate.place(x=50, y=315)

		txt_paydate=Entry(self.root, textvariable=self.var_paydate, font=("goudy old style", 15), bg="lightyellow")
		txt_paydate.place(x=150, y=315, width=180)

		#====Buttons======================================================
		btn_add=Button(self.root, command=self.add, text="Save", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#2196f3")
		btn_add.place(x=150, y=380, width=100, height=32)
	
		btn_update=Button(self.root, command=self.update, text="Update", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#4caf50")
		btn_update.place(x=270, y=380, width=100, height=32)
	
		btn_delete=Button(self.root, command=self.delete, text="Delete", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#f44336")
		btn_delete.place(x=390, y=380, width=100, height=32)
	
		btn_clear=Button(self.root, command=self.clear, text="Clear", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#607d8b")
		btn_clear.place(x=510, y=380, width=100, height=32)


		#===Credit Details Frame=================
		credit_frame=Frame(self.root, bd=3, relief=RIDGE)
		credit_frame.place(x=680, y=120, width=380, height=350)

		scrolly=Scrollbar(credit_frame, orient=VERTICAL)
		scrollx=Scrollbar(credit_frame, orient=HORIZONTAL)

		self.creditTable=ttk.Treeview(credit_frame, columns=("name", "product", "qty", "price", "total", "paydate"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM, fill=X)
		scrolly.pack(side=RIGHT, fill=Y)
		scrollx.config(command=self.creditTable.xview)
		scrolly.config(command=self.creditTable.yview)
		self.creditTable.heading("name", text="Name")
		self.creditTable.heading("product", text="Product")
		self.creditTable.heading("qty", text="Qty")
		self.creditTable.heading("price", text="Price")
		self.creditTable.heading("total", text="Total")
		self.creditTable.heading("paydate", text="PayDate")
		
		self.creditTable["show"]="headings"

		self.creditTable.column("name", width=90)
		self.creditTable.column("product", width=100)
		self.creditTable.column("qty", width=70)
		self.creditTable.column("price", width=100)
		self.creditTable.column("total", width=100)
		self.creditTable.column("paydate", width=80)
		self.creditTable.pack(fill=BOTH, expand=1)
		self.creditTable.bind("<ButtonRelease-1>", self.get_data) # when clicked ones on table, perform whats in getdata function.
		self.show()


		#===database CRUD=================
	def add(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_name.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Customer name is required", parent=self.root)
			else:
				cur.execute("SELECT * FROM credit WHERE name=?", (self.var_name.get(),))
				row = cur.fetchone()
				if row!=None:
					messagebox.showerror("Error", "Name Already Assigned, use a Different Name", parent=self.root)
				else:
					cur.execute("INSERT INTO credit(name, product, qty, price, total, paydate) values(?,?,?,?,?,?)",(
										self.var_name.get(),
										self.var_product.get(),
										self.var_qty.get(),
										self.var_price.get(),
										self.var_total.get(),
										self.var_paydate.get(),
										
										
					))
					con.commit()
					messagebox.showinfo("Success", "Customer Added Successfully!!", parent=self.root)
					self.show() #display the added info in treeview frame after displaying sucess message 
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def show(self): #function for showing data in the treeview frame
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT * FROM credit")
			rows=cur.fetchall()
			self.creditTable.delete(*self.creditTable.get_children()) ##get all the rows inside the treeview table and delete them
			for row in rows:
				self.creditTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview

			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def get_data(self,ev): #function for binding selectedrow i.e wen we click on a row it shows in the entry boxes
		f=self.creditTable.focus()
		content=(self.creditTable.item(f))
		row=content['values']
		#print(row)
		self.var_name.set(row[0]) #these will allow the values of the rows selected to pop up in the entry widgets
		self.var_product.set(row[1])
		self.var_qty.set(row[2])
		self.var_price.set(row[3])
		self.var_total.set(row[4])
		self.var_paydate.set(row[5])


	#=========Update===========================
	def update(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_name.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Customer Name required", parent=self.root)
			else:
				cur.execute("SELECT * FROM credit WHERE name=?", (self.var_name.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! This Name does not exist", parent=self.root)
				else:
					cur.execute("UPDATE credit SET product=?, qty=?, price=?, total=?, paydate=? WHERE name=?",(
								
										self.var_product.get(),
										self.var_qty.get(),
										self.var_price.get(),
										self.var_total.get(),
										self.var_paydate.get(),
										self.var_name.get()

					))					
					con.commit()
					messagebox.showinfo("Success", "Credit Details Updated Successfully!!", parent=self.root)
					self.show() #display the added info in treeview frame after displaying sucess message 
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#=============Delete record================
	def delete(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_name.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Customer Name required", parent=self.root)
			else:
				cur.execute("SELECT * FROM credit WHERE name=?", (self.var_name.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! This Name does not exist", parent=self.root)
				else:
					op=messagebox.askyesno("Confirm", "Are you sure you want to delete this Customer?", parent=self.root)
					if op==True:
						cur.execute("DELETE FROM credit WHERE name=?", (self.var_name.get(),))
						con.commit()
						messagebox.showinfo("Delete", "Customer Deleted Successfully", parent=self.root)
						self.clear()
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#==========Clear all records=============
	def clear(self):
		self.var_name.set("") 
		self.var_product.set("")
		self.var_qty.set("")
		self.var_price.set("")
		self.var_total.set("")
		self.var_paydate.set("")
		
		self.show()

#========search from database==========
	def search(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_searchtxt.get()=="":
				messagebox.showerror("Error", "Customer Name required", parent=self.root)
			else:
				cur.execute("SELECT name, product, qty, price, total, paydate FROM credit WHERE name Like '%"+self.var_searchtxt.get()+"%'")
				row=cur.fetchone()
				if row!=None:
					self.creditTable.delete(*self.creditTable.get_children()) ##get all the rows inside the treeview table and delete them
					self.creditTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview
				else:
					messagebox.showerror("Error", "No record found, Input a correct Customer Name", parent=self.root)
			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__=="__main__":
	root=Tk()
	obj=creditClass(root)
	root.mainloop()

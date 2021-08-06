from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class productClass:
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


		self.var_pid=StringVar()
		self.var_cat=StringVar()
		self.var_sup=StringVar()
		self.cat_list=[]
		self.sup_list=[]
		self.fetch_cat_sup()
		self.var_name=StringVar()
		self.var_price=StringVar()
		self.var_qty=StringVar()
		self.var_status=StringVar()
		self.var_serial=StringVar()
	

		#===product frame======
		product_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
		product_Frame.place(x=10, y=10, width=450, height=480)

		#====title/labels=========================
		title=Label(product_Frame, text="Manage Product Details", font=("goudy old style", 18), bg="#4b100a", fg="white")
		title.pack(side=TOP, fill=X)

		lbl_category=Label(product_Frame, text="Category", font=("goudy old style", 18), bg="white")
		lbl_category.place(x=30, y=50)

		lbl_supplier=Label(product_Frame, text="Supplier", font=("goudy old style", 18), bg="white")
		lbl_supplier.place(x=30, y=100)

		lbl_product_name=Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white")
		lbl_product_name.place(x=30, y=150)

		lbl_price=Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white")
		lbl_price.place(x=30, y=200)

		lbl_quantity=Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white")
		lbl_quantity.place(x=30, y=250)

		lbl_status=Label(product_Frame, text="Status", font=("goudy old style", 18), bg="white")
		lbl_status.place(x=30, y=300)

		#lbl_serial=Label(product_Frame, text="Serial No.", font=("goudy old style", 18), bg="white")
		#lbl_serial.place(x=30, y=350)

		#====Entries========
		cmb_cat=ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state="readonly", justify=CENTER, font=("goudy old style", 15))
		cmb_cat.place(x=150, y=50, width=200)
		cmb_cat.current(0)

		cmb_sup=ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state="readonly", justify=CENTER, font=("goudy old style", 15))
		cmb_sup.place(x=150, y=100, width=200)
		cmb_sup.current(0)

		txt_name=Entry(product_Frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
		txt_name.place(x=150, y=150, width=200)

		txt_price=Entry(product_Frame, textvariable=self.var_price, font=("goudy old style", 15), bg="lightyellow")
		txt_price.place(x=150, y=200, width=200)

		txt_qty=Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style", 15), bg="lightyellow")
		txt_qty.place(x=150, y=250, width=200)

		cmb_status=ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state="readonly", justify=CENTER, font=("goudy old style", 15))
		cmb_status.place(x=150, y=300, width=200)
		cmb_status.current(0)

		#txt_serial=Entry(product_Frame, textvariable=self.var_serial, font=("goudy old style", 15), bg="lightyellow")
		#txt_serial.place(x=150, y=350, width=200)

		#====Buttons======================================================
		btn_add=Button(product_Frame, command=self.add, text="Save", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#2196f3")
		btn_add.place(x=10, y=410, width=100, height=38)
	
		btn_update=Button(product_Frame, command=self.update, text="Update", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#4caf50")
		btn_update.place(x=120, y=410, width=100, height=38)
	
		btn_delete=Button(product_Frame, command=self.delete, text="Delete", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#f44336")
		btn_delete.place(x=230, y=410, width=100, height=38)
	
		btn_clear=Button(product_Frame, command=self.clear, text="Clear", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#607d8b")
		btn_clear.place(x=340, y=410, width=100, height=38)
		
		#===search frame===============
		searchFrame=LabelFrame(self.root, text="Search Product", font=("goudy old style",12,"bold"), bd=2, relief=RIDGE, bg="white")
		searchFrame.place(x=480, y=10, width=600, height=80)

		#===options for combobox=============
		cmb_search=ttk.Combobox(searchFrame,  textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"), state="readonly", justify=CENTER, font=("goudy old style", 15))
		cmb_search.place(x=10, y=10, width=180)
		cmb_search.current(0)

		txt_search=Entry(searchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
		txt_search.place(x=200, y=10)

		btn_search=Button(searchFrame, command=self.search, text="Search", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#4caf50")
		btn_search.place(x=440, y=10, width=120, height=26)


		#===Product Details Frame=================
		p_frame=Frame(self.root, bd=3, relief=RIDGE)
		p_frame.place(x=480, y=100, width=600, height=390)

		scrolly=Scrollbar(p_frame, orient=VERTICAL)
		scrollx=Scrollbar(p_frame, orient=HORIZONTAL)

		self.product_table=ttk.Treeview(p_frame, columns=("pid", "Supplier", "Category", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM, fill=X)
		scrolly.pack(side=RIGHT, fill=Y)
		scrollx.config(command=self.product_table.xview)
		scrolly.config(command=self.product_table.yview)
		self.product_table.heading("pid", text="ID")
		self.product_table.heading("Category", text="Category")
		self.product_table.heading("Supplier", text="Supplier")
		self.product_table.heading("name", text="Name")
		self.product_table.heading("price", text="Price")
		self.product_table.heading("qty", text="Qty")
		self.product_table.heading("status", text="Status")
		#self.product_table.heading("serialNo", text="SerialNo")

		self.product_table["show"]="headings"

		self.product_table.column("pid", width=90)
		self.product_table.column("Category", width=100)
		self.product_table.column("Supplier", width=100)
		self.product_table.column("name", width=100)
		self.product_table.column("price", width=100)
		self.product_table.column("qty", width=100)
		self.product_table.column("status", width=100)
		#self.product_table.column("serialNo", width=100)
		self.product_table.pack(fill=BOTH, expand=1)
		self.product_table.bind("<ButtonRelease-1>", self.get_data) # when clicked ones on table, perform whats in getdata function.

		self.show()
	


		#====DataBase CRUD=====================
	def fetch_cat_sup(self):
		self.cat_list.append("Empty")# first put empty in the list
		self.sup_list.append("Empty")# first put empty in the list
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT name FROM category")
			cat=cur.fetchall()
			if len(cat)>0:
				del self.cat_list[:] #if what we fetch from the table is >0, remove "Empty" from the list
				self.cat_list.append("Select") #if row is morethan 1 in category table, put Select in list before looping
				for i in cat:
					self.cat_list.append(i[0])


			cur.execute("SELECT name FROM supplier")
			sup=cur.fetchall()
			if len(sup)>0:
				del self.sup_list[:] #if what we fetch from the table is >0, remove "Empty" from the list
				self.sup_list.append("Select") #if row is morethan 1 in category table, put Select in list before looping
				for i in sup:
					self.sup_list.append(i[0])

		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


	def add(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":	#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Category,Supplier and Name of product are required", parent=self.root)
			else:
				cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
				row = cur.fetchone()
				if row!=None:
					messagebox.showerror("Error", "Product Already Exist!", parent=self.root)
				else:
					cur.execute("INSERT INTO product(Supplier, Category, name, price, qty, status) values(?,?,?,?,?,?)",(		
										self.var_sup.get(),
										self.var_cat.get(),
										self.var_name.get(),
										self.var_price.get(),
										self.var_qty.get(),
										self.var_status.get(),
										#self.var_serial.get(),
										
					))
					con.commit()
					messagebox.showinfo("Success", "Product Added Successfully!!", parent=self.root)
					self.show() #display the added info in treeview frame after displaying sucess message 
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def show(self): #function for showing data in the treeview frame
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT * FROM product")
			rows=cur.fetchall()
			self.product_table.delete(*self.product_table.get_children()) ##get all the rows inside the treeview table and delete them
			for row in rows:
				self.product_table.insert('', END, values=row)    ##Display rows selected from the database in the treeview

			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def get_data(self,ev): #function for binding selectedrow i.e wen we click on a row it shows in the entry boxes
		f=self.product_table.focus()
		content=(self.product_table.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_sup.set(row[1])
		self.var_cat.set(row[2])
		self.var_name.set(row[3])
		self.var_price.set(row[4])
		self.var_qty.set(row[5])
		self.var_status.set(row[6])
		#self.var_serial.set(row[7])
		
#=========Update===========================
	def update(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_pid.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Please Select Product From Table", parent=self.root)
			else:
				cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! Product does not exist", parent=self.root)
				else:
					cur.execute("UPDATE product SET Supplier=?, Category=?, name=?, price=?, qty=?, status=? WHERE pid=?",(
								
										self.var_sup.get(),
										self.var_cat.get(),
										self.var_name.get(),
										self.var_price.get(),
										self.var_qty.get(),
										self.var_status.get(),
										#self.var_serial.get(),
										self.var_pid.get()

					))					
					con.commit()
					messagebox.showinfo("Success", "Product Updated Successfully!!", parent=self.root)
					self.show() #display the added info in treeview frame after displaying sucess message 
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#=============Delete record================
	def delete(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_pid.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Please Select Product From Table", parent=self.root)
			else:
				cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! Product does not exist", parent=self.root)
				else:
					op=messagebox.askyesno("Confirm", "Are you sure you want to delete this Product?", parent=self.root)
					if op==True:
						cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
						con.commit()
						messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
						self.clear()
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#==========Clear all records=============
	def clear(self):
		self.var_sup.set("Select")
		self.var_cat.set("Select")
		self.var_name.set("")
		self.var_price.set("")
		self.var_qty.set("")
		self.var_status.set("Active")
		#self.var_serial.set("")
		self.var_pid.set("")
		
		self.var_searchtxt.set("")
		self.var_searchby.set("Select")
		self.show()

#========search from database==========
	def search(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_searchby.get()=="Select":
				messagebox.showerror("Error", "Please Choose a Search Option from the Dropdown Menu", parent=self.root)
			elif self.var_searchtxt.get()=="":
				messagebox.showerror("Error", "Search input required", parent=self.root)
			else:
				cur.execute("SELECT * FROM product WHERE "+self.var_searchby.get()+" Like '%"+self.var_searchtxt.get()+"%'")
				rows=cur.fetchall()
				if len(rows)!=0:
					self.product_table.delete(*self.product_table.get_children()) ##get all the rows inside the treeview table and delete them
					for row in rows:
						self.product_table.insert('', END, values=row)    ##Display rows selected from the database in the treeview
				else:
					messagebox.showerror("Error", "No record found, Try other Select options", parent=self.root)
			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)






if __name__=="__main__":
	root=Tk()
	obj=productClass(root)
	root.mainloop()

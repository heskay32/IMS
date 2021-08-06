from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class supplierClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+130")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | Inventory Management System |   Developed By Olasunkanmi")
		self.root.config(bg="white")
		self.root.focus_force()
		#==============================================================================
		#All Variables for content area======================
		self.var_searchby=StringVar()
		self.var_searchtxt=StringVar()


		self.var_sup_invoice=StringVar()
		self.var_name=StringVar()
		self.var_contact=StringVar()
		
		
		#===search frame===============
		
		#===options=============
		lbl_search=Label(self.root, text="Invoice No.", bg="white", font=("goudy old style", 15))
		lbl_search.place(x=680, y=90)
	

		txt_search=Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
		txt_search.place(x=780, y=90, width=150)

		btn_search=Button(self.root, command=self.search, text="Search", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#4caf50")
		btn_search.place(x=960, y=89, width=100, height=27)

		#====title=========================
		title=Label(self.root, text="Manage Supplier Details", font=("goudy old style", 23, "bold"), bg="#4b100a", fg="white")
		title.place(x=50, y=10, width=1000, height=50)

		#====content=========
		#1st row==
		lbl_supplier_invoice=Label(self.root, text="Invoice No:", font=("goudy old style", 15), bg="white")
		lbl_supplier_invoice.place(x=50, y=90)

		txt_supplier_invoice=Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow")
		txt_supplier_invoice.place(x=150, y=90, width=180)

		#2nd row==
		lbl_name=Label(self.root, text="Name", font=("goudy old style", 15), bg="white")
		lbl_name.place(x=50, y=135)

		txt_name=Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
		txt_name.place(x=150, y=135, width=180)

		#3rd row==
		lbl_contact=Label(self.root, text="Contact", font=("goudy old style", 15), bg="white")
		lbl_contact.place(x=50, y=180)

		txt_contact=Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow")
		txt_contact.place(x=150, y=180, width=180)

		#4th row==
		lbl_desc=Label(self.root, text="Description", font=("goudy old style", 15), bg="white")
		lbl_desc.place(x=50, y=225)

		self.txt_desc=Text(self.root, font=("goudy old style", 15), bg="lightyellow")
		self.txt_desc.place(x=150, y=225, width=462, height=80)

		#====Buttons======================================================
		btn_add=Button(self.root, command=self.add, text="Save", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#2196f3")
		btn_add.place(x=150, y=350, width=100, height=32)
	
		btn_update=Button(self.root, command=self.update, text="Update", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#4caf50")
		btn_update.place(x=270, y=350, width=100, height=32)
	
		btn_delete=Button(self.root, command=self.delete, text="Delete", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#f44336")
		btn_delete.place(x=390, y=350, width=100, height=32)
	
		btn_clear=Button(self.root, command=self.clear, text="Clear", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#607d8b")
		btn_clear.place(x=510, y=350, width=100, height=32)
		
		#===Supplier Details Frame=================
		emp_frame=Frame(self.root, bd=3, relief=RIDGE)
		emp_frame.place(x=680, y=120, width=380, height=350)

		scrolly=Scrollbar(emp_frame, orient=VERTICAL)
		scrollx=Scrollbar(emp_frame, orient=HORIZONTAL)

		self.supplierTable=ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM, fill=X)
		scrolly.pack(side=RIGHT, fill=Y)
		scrollx.config(command=self.supplierTable.xview)
		scrolly.config(command=self.supplierTable.yview)
		self.supplierTable.heading("invoice", text="Invoice No.")
		self.supplierTable.heading("name", text="Name")
		self.supplierTable.heading("contact", text="Contact")
		self.supplierTable.heading("desc", text="Description")
		
		self.supplierTable["show"]="headings"

		self.supplierTable.column("invoice", width=90)
		self.supplierTable.column("name", width=100)
		self.supplierTable.column("contact", width=100)
		self.supplierTable.column("desc", width=100)
		self.supplierTable.pack(fill=BOTH, expand=1)
		self.supplierTable.bind("<ButtonRelease-1>", self.get_data) # when clicked ones on table, perform whats in getdata function.

		self.show() #display everything in the employee table inside the treeview frame.
#==================================================================================================================================================
		#===database CRUD=================
	def add(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_sup_invoice.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Invoice is required", parent=self.root)
			else:
				cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
				row = cur.fetchone()
				if row!=None:
					messagebox.showerror("Error", "Invoice Number Already Assigned!", parent=self.root)
				else:
					cur.execute("INSERT INTO supplier(invoice, name, contact, desc) values(?,?,?,?)",(
										self.var_sup_invoice.get(),
										self.var_name.get(),
										self.var_contact.get(),
										self.txt_desc.get('1.0',END),
										
					))
					con.commit()
					messagebox.showinfo("Success", "Supplier Added Successfully!!", parent=self.root)
					self.show() #display the added info in treeview frame after displaying sucess message 
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def show(self): #function for showing data in the treeview frame
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT * FROM supplier")
			rows=cur.fetchall()
			self.supplierTable.delete(*self.supplierTable.get_children()) ##get all the rows inside the treeview table and delete them
			for row in rows:
				self.supplierTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview

			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def get_data(self,ev): #function for binding selectedrow i.e wen we click on a row it shows in the entry boxes
		f=self.supplierTable.focus()
		content=(self.supplierTable.item(f))
		row=content['values']
		#print(row)
		self.var_sup_invoice.set(row[0]) #these will allow the values of the rows selected to pop up in the entry widgets
		self.var_name.set(row[1])
		self.var_contact.set(row[2])
		self.txt_desc.delete('1.0',END)
		self.txt_desc.insert(END, row[3])
	

#=========Update===========================
	def update(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_sup_invoice.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Invoice is required", parent=self.root)
			else:
				cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! Invoice No. does not exist", parent=self.root)
				else:
					cur.execute("UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",(
								
										self.var_name.get(),
										self.var_contact.get(),
										self.txt_desc.get('1.0',END),
										self.var_sup_invoice.get()

					))					
					con.commit()
					messagebox.showinfo("Success", "Supplier Updated Successfully!!", parent=self.root)
					self.show() #display the added info in treeview frame after displaying sucess message 
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#=============Delete record================
	def delete(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_sup_invoice.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Invoice is required", parent=self.root)
			else:
				cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! Invoice No. does not exist", parent=self.root)
				else:
					op=messagebox.askyesno("Confirm", "Are you sure you want to delete this Supplier?", parent=self.root)
					if op==True:
						cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
						con.commit()
						messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
						self.clear()
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#==========Clear all records=============
	def clear(self):
		self.var_sup_invoice.set("") 
		self.var_name.set("")
		self.var_contact.set("")
		self.txt_desc.delete('1.0',END)
		self.var_searchtxt.set("")
		self.show()

#========search from database==========
	def search(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_searchtxt.get()=="":
				messagebox.showerror("Error", "Invoice No. required", parent=self.root)
			else:
				cur.execute("SELECT * FROM supplier WHERE invoice=?",(self.var_searchtxt.get(),))
				row=cur.fetchone()
				if row!=None:
					self.supplierTable.delete(*self.supplierTable.get_children()) ##get all the rows inside the treeview table and delete them
					self.supplierTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview
				else:
					messagebox.showerror("Error", "No record found, Input a correct Invoice No.", parent=self.root)
			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



if __name__=="__main__":
	root=Tk()
	obj=supplierClass(root)
	root.mainloop()

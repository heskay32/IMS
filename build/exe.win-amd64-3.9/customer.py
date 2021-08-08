from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class customerClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("700x400+220+130")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | Customer Details |   Developed By Olasunkanmi")
		self.root.config(bg="white")
		self.root.resizable(False,False)
		#===========================================================

		self.var_searchtxt=StringVar()

		self.var_cuid=StringVar()
		self.var_cname=StringVar()
		self.var_contact=StringVar()
		
		#===search area=========
		lbl_search=Label(self.root, text="Customer No", bg="white", font=("goudy old style", 15))
		lbl_search.place(x=295, y=80)
	

		txt_search=Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
		txt_search.place(x=420, y=80, width=150)

		btn_search=Button(self.root, command=self.search, text="Search", font=("goudy old style", 15),cursor="hand2", fg="white", bg="#4caf50")
		btn_search.place(x=575, y=80, width=100, height=27)


		#====title=========================
		title=Label(self.root, text="Manage Customer", font=("goudy old style", 23, "bold"), bg="#4b100a", fg="white")
		title.place(x=20, y=10, width=650, height=50)

		#1st row==
		lbl_cuid=Label(self.root, text="ID", font=("goudy old style", 15), bg="white")
		lbl_cuid.place(x=50, y=145)

		txt_cuid=Entry(self.root, textvariable=self.var_cuid, font=("goudy old style", 15), bg="lightyellow")
		txt_cuid.place(x=150, y=145, width=180)


		lbl_name=Label(self.root, text="Name", font=("goudy old style", 15), bg="white")
		lbl_name.place(x=50, y=190)

		txt_name=Entry(self.root, textvariable=self.var_cname, font=("goudy old style", 15), bg="lightyellow")
		txt_name.place(x=150, y=190, width=180)

		#2nd row==
		lbl_contact=Label(self.root, text="Contact", font=("goudy old style", 15), bg="white")
		lbl_contact.place(x=50, y=235)

		txt_contact=Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow")
		txt_contact.place(x=150, y=235, width=180)


		btn_update=Button(self.root, command=self.update, text="Update", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#4caf50")
		btn_update.place(x=50, y=330, width=75, height=27)
	
		btn_delete=Button(self.root, command=self.delete, text="Delete", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#f44336")
		btn_delete.place(x=140, y=330, width=75, height=27)
	
		btn_clear=Button(self.root, command=self.clear, text="Clear", font=("goudy old style", 17),cursor="hand2", fg="white", bg="#607d8b")
		btn_clear.place(x=230, y=330, width=75, height=27)

		#===Customer Details Frame=================
		customer_frame=Frame(self.root, bd=3, relief=RIDGE)
		customer_frame.place(x=350, y=110, width=330, height=250)

		scrolly=Scrollbar(customer_frame, orient=VERTICAL)
		scrollx=Scrollbar(customer_frame, orient=HORIZONTAL)

		self.customerTable=ttk.Treeview(customer_frame, columns=("cuid", "name", "number"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM, fill=X)
		scrolly.pack(side=RIGHT, fill=Y)
		scrollx.config(command=self.customerTable.xview)
		scrolly.config(command=self.customerTable.yview)
		self.customerTable.heading("cuid", text="ID")
		self.customerTable.heading("name", text="Name")
		self.customerTable.heading("number", text="Contact")
			
		self.customerTable["show"]="headings"

		self.customerTable.column("cuid", width=50)
		self.customerTable.column("name", width=120)
		self.customerTable.column("number", width=80)
		self.customerTable.pack(fill=BOTH, expand=1)
		self.customerTable.bind("<ButtonRelease-1>", self.get_data) # when clicked ones on table, perform whats in getdata function.
		self.show()


	def show(self): #function for showing data in the treeview frame
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT * FROM customer")
			rows=cur.fetchall()
			self.customerTable.delete(*self.customerTable.get_children()) ##get all the rows inside the treeview table and delete them
			for row in rows:
				self.customerTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview

			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def get_data(self,ev): #function for binding selectedrow i.e wen we click on a row it shows in the entry boxes
		f=self.customerTable.focus()
		content=(self.customerTable.item(f))
		row=content['values']
		#print(row)
		self.var_cuid.set(row[0])
		self.var_cname.set(row[1]) #these will allow the values of the rows selected to pop up in the entry widgets
		self.var_contact.set(row[2])
		

	#=========Update===========================
	def update(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_contact.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Search and Select Customer From the Table", parent=self.root)
			else:
				cur.execute("SELECT * FROM customer WHERE cuid=?", (self.var_cuid.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! Customer does not exist\nStart contact with +234", parent=self.root)
				else:
					cur.execute("UPDATE customer SET number=? WHERE cuid=?",(
								
										self.var_contact.get(),
										self.var_cuid.get()
										

					))					
					con.commit()
					messagebox.showinfo("Success", "Customer Details Updated Successfully!!", parent=self.root)
					self.show() #display the added info in treeview frame after displaying sucess message 
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#=============Delete record================
	def delete(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_contact.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Search and Select Customer From the Table", parent=self.root)
			else:
				cur.execute("SELECT * FROM customer WHERE cuid=?", (self.var_cuid.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! Customer does not exist", parent=self.root)
				else:
					op=messagebox.askyesno("Confirm", "Are you sure you want to delete this Customer?", parent=self.root)
					if op==True:
						cur.execute("DELETE FROM customer WHERE cuid=?", (self.var_cuid.get(),))
						con.commit()
						messagebox.showinfo("Delete", "Customer Deleted Successfully", parent=self.root)
						self.clear()
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


#==========Clear all records=============
	def clear(self):
		self.var_cname.set("") 
		self.var_cuid.set("")
		self.var_contact.set("")
		
		self.show()

#========search from database==========
	def search(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_searchtxt.get()=="":
				messagebox.showerror("Error", "Customer Contact required", parent=self.root)
			else:
				cur.execute("SELECT cuid, name, number FROM customer WHERE number Like '%"+self.var_searchtxt.get()+"%'")
				row=cur.fetchone()
				if row!=None:
					self.customerTable.delete(*self.customerTable.get_children()) ##get all the rows inside the treeview table and delete them
					self.customerTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview
				else:
					messagebox.showerror("Error", "No record found, Input a correct Customer Contact Details", parent=self.root)
			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)




if __name__=="__main__":
	root=Tk()
	obj=customerClass(root)
	root.mainloop()

from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class categoryClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+130")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | Inventory Management System |   Developed By Olasunkanmi")
		self.root.config(bg="white")
		self.root.focus_force()

		#===String Variables=========
		self.var_cat_id=StringVar()
		self.var_name=StringVar()


		#======title===============
		lbl_title=Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#4b100a", fg="white", bd=1, relief=RIDGE)
		lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

		lbl_name=Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="white")
		lbl_name.place(x=50, y=100)

		txt_name=Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="lightyellow")
		txt_name.place(x=50, y=170, width=300)

		btn_add=Button(self.root, command=self.add, text="ADD", font=("goudy old style", 18), bg="#4caf50", fg="white", cursor="hand2")
		btn_add.place(x=360, y=170, width=150, height=30)

		btn_delete=Button(self.root, command=self.delete, text="Delete", font=("goudy old style", 18), bg="red", fg="white", cursor="hand2")
		btn_delete.place(x=520, y=170, width=150, height=30)


		#===Category Details Frame=================
		cat_frame=Frame(self.root, bd=3, relief=RIDGE)
		cat_frame.place(x=680, y=120, width=380, height=350)

		scrolly=Scrollbar(cat_frame, orient=VERTICAL)
		scrollx=Scrollbar(cat_frame, orient=HORIZONTAL)

		self.categoryTable=ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM, fill=X)
		scrolly.pack(side=RIGHT, fill=Y)
		scrollx.config(command=self.categoryTable.xview)
		scrolly.config(command=self.categoryTable.yview)
		self.categoryTable.heading("cid", text="ID")
		self.categoryTable.heading("name", text="Name")
		
		self.categoryTable["show"]="headings"

		self.categoryTable.column("cid", width=90)
		self.categoryTable.column("name", width=100)
		self.categoryTable.pack(fill=BOTH, expand=1)
		self.categoryTable.bind("<ButtonRelease-1>", self.get_data) # when clicked ones on table, perform whats in getdata function.

		self.show()#display everything in the employee table inside the treeview frame.

		#===images======
		self.im1=Image.open("images/distribution.png")
		self.im1=self.im1.resize((615,246), Image.ANTIALIAS)
		self.im1=ImageTk.PhotoImage(self.im1)

		self.lbl_im1=Label(self.root, image=self.im1)
		self.lbl_im1.place(x=50, y=220)

		#=====Database=====
	def add(self):
			con = sqlite3.connect(database=r'ims.db')
			cur = con.cursor()
			try:
				if self.var_name.get()=="":			#means if what is typed in the EMP ID feild is empty
					messagebox.showerror("Error", "Category Name is required", parent=self.root)
				else:
					cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
					row = cur.fetchone()
					if row!=None:
						messagebox.showerror("Error", "Category Already Exists!", parent=self.root)
					else:
						cur.execute("INSERT INTO category(name) values(?)",(
											
											self.var_name.get(),
											
						))
						con.commit()
						messagebox.showinfo("Success", "Category Added Successfully!!", parent=self.root)
						self.show() #display the added info in treeview frame after displaying sucess message 
			except Exception as ex:
				messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



	def show(self): #function for showing data in the treeview frame
			con = sqlite3.connect(database=r'ims.db')
			cur = con.cursor()
			try:
				cur.execute("SELECT * FROM category")
				rows=cur.fetchall()
				self.categoryTable.delete(*self.categoryTable.get_children()) ##get all the rows inside the treeview table and delete them
				for row in rows:
					self.categoryTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview

				
			except Exception as ex:
				messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



	def get_data(self,ev): #function for binding selectedrow i.e wen we click on a row it shows in the entry boxes
			f=self.categoryTable.focus()
			content=(self.categoryTable.item(f))
			row=content['values']
			#print(row)
			self.var_cat_id.set(row[0]) #these will allow the values of the rows selected to pop up in the entry widgets
			self.var_name.set(row[1])
		

	def delete(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_name.get()=="":			#means if what is typed in the EMP ID feild is empty
				messagebox.showerror("Error", "Error!! Please select category from the table", parent=self.root)
			else:
				cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
				row = cur.fetchone()
				if row==None:
					messagebox.showerror("Error", "Invalid!!! Category name does not exist", parent=self.root)
				else:
					op=messagebox.askyesno("Confirm", "Are you sure you want to delete this Category?", parent=self.root)
					if op==True:
						cur.execute("DELETE FROM category WHERE name=?", (self.var_name.get(),))
						con.commit()
						messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
						self.clear()
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


	def clear(self):
		self.var_cat_id.set("") 
		self.var_name.set("")
		self.show()



if __name__=="__main__":
	root=Tk()
	obj=categoryClass(root)
	root.mainloop()

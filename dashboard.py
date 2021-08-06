from tkinter import*
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from credit import creditClass
import sqlite3
from tkinter import messagebox
import os
import time
class IMS:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1350x700+0+0")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | Inventory Management System |   Developed By Olasunkanmi")
		self.root.config(bg="lightgrey")
		#====title===
		self.icon_title=PhotoImage(file="images/logoo.png")
		title = Label(self.root, text="KING's POWER TECH Inventory Management System", image=self.icon_title, compound=LEFT, font=("times new roman", 30, "bold"), bg="#c0392b", fg="white", anchor="w", padx=20)
		title.place(x=0, y=0, relwidth=1, height=70)

		#===btn_logout====
		btn_logout = Button(self.root, command=self.logout, bg="yellow", fg='black', text="Logout", font=("times new roman", 15, "bold"), cursor="hand2", bd=1)
		btn_logout.place(x=1185, y=16, height=40, width=100)

		#===clock and date=======
		self.lbl_clock = Label(self.root, text="Welcome to King's Power Tech IMS\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#4b100a", fg="white")
		self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

		#===left menu========
		self.MenuLogo = Image.open("images/menulogo.png")
		self.MenuLogo = self.MenuLogo.resize((200,200), Image.ANTIALIAS)
		self.MenuLogo =ImageTk.PhotoImage(self.MenuLogo)
		LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
		LeftMenu.place(x=0, y=102, width=200, height=550)

		lbl_menulogo = Label(LeftMenu, image=self.MenuLogo)
		lbl_menulogo.pack(side=TOP, fill=X)

		lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#c0392b")
		lbl_menu.pack(side=TOP, fill=X)

		#===left menu buttons=======
		self.icon_side = PhotoImage(file="images/logoo.png")
		btn_employee = Button(LeftMenu, text="Employee", command=self.employee, font=("times new roman", 20, "bold"), bg="#4b100a", bd=3, fg="white", cursor="hand2")
		btn_employee.place(x=0, y=238, width=200, height=50)

		btn_supplier = Button(LeftMenu, command=self.supplier, text="Supplier", font=("times new roman", 20, "bold"), bg="#4b100a", bd=3, fg="white", cursor="hand2")
		btn_supplier.place(x=0, y=290, width=200, height=50)

		btn_category = Button(LeftMenu, command=self.category, text="Category", font=("times new roman", 20, "bold"), bg="#4b100a", bd=3, fg="white", cursor="hand2")
		btn_category.place(x=0, y=342, width=200, height=50)

		btn_products = Button(LeftMenu, command=self.product, text="Products", font=("times new roman", 20, "bold"), bg="#4b100a", bd=3, fg="white", cursor="hand2")
		btn_products.place(x=0, y=394, width=200, height=50)

		btn_sales = Button(LeftMenu, command=self.sales, text="Sales", font=("times new roman", 20, "bold"), bg="#4b100a", bd=3, fg="white", cursor="hand2")
		btn_sales.place(x=0, y=446, width=200, height=50)

		btn_credits = Button(LeftMenu, command=self.credit, text="Credits", font=("times new roman", 20, "bold"), bg="#4b100a", bd=3, fg="white", cursor="hand2")
		btn_credits.place(x=0, y=498, width=200, height=50)

		#=======middle content===========
		self.productLogo=Image.open("images/cartCL.png")
		self.productLogo = self.productLogo.resize((170,110), Image.ANTIALIAS)
		self.productLogo =ImageTk.PhotoImage(self.productLogo)

		self.employeeLogo=Image.open("images/employee1.png")
		self.employeeLogo = self.employeeLogo.resize((170,110), Image.ANTIALIAS)
		self.employeeLogo =ImageTk.PhotoImage(self.employeeLogo)

		self.salesLogo=Image.open("images/sales3.png")
		self.salesLogo = self.salesLogo.resize((170,110), Image.ANTIALIAS)
		self.salesLogo =ImageTk.PhotoImage(self.salesLogo)


		self.supplierLogo=Image.open("images/supplier1.png")
		self.supplierLogo = self.supplierLogo.resize((170,110), Image.ANTIALIAS)
		self.supplierLogo =ImageTk.PhotoImage(self.supplierLogo)

		self.categoryLogo=Image.open("images/category.png")
		self.categoryLogo = self.categoryLogo.resize((170,110), Image.ANTIALIAS)
		self.categoryLogo =ImageTk.PhotoImage(self.categoryLogo)

		self.creditLogo=Image.open("images/credit.png")
		self.creditLogo = self.creditLogo.resize((170,110), Image.ANTIALIAS)
		self.creditLogo =ImageTk.PhotoImage(self.creditLogo)


		self.lbl_employee=Label(self.root, text="Total Employee\n[ 0 ]", bd=1, relief=RIDGE, bg="blue", fg="black", font=("goundy old style", 20, "bold"),image=self.employeeLogo, compound="bottom", anchor="w", padx=20)
		self.lbl_employee.place(x=300, y=120, height=160, width=300)

		self.lbl_supplier=Label(self.root, text="Total Supplier\n[ 0 ]", bd=1, relief=RIDGE, bg="lightgreen", fg="black", font=("goundy old style", 20, "bold"),image=self.supplierLogo, compound="bottom", anchor="w", padx=20)
		self.lbl_supplier.place(x=650, y=120, height=160, width=300)

		self.lbl_category=Label(self.root, text="Total category\n[ 0 ]", bd=1, relief=RIDGE, bg="lightcyan", fg="black", font=("goundy old style", 20, "bold"),image=self.categoryLogo, compound="bottom", anchor="w", padx=20)
		self.lbl_category.place(x=1000, y=120, height=160, width=300)

		self.lbl_product=Label(self.root, text="Total Product[ 0 ]", bd=1, relief=RIDGE, bg="lightblue", fg="black", font=("goundy old style", 20, "bold"), image=self.productLogo, compound="bottom", anchor="w", padx=20)
		self.lbl_product.place(x=300, y=300, height=160, width=300)

		self.lbl_sales=Label(self.root, text="Total Sales\n[ 0 ]", bd=1, relief=RIDGE, bg="greenyellow", fg="black", font=("goundy old style", 20, "bold"),image=self.salesLogo, compound="bottom", anchor="w", padx=20)
		self.lbl_sales.place(x=650, y=300, height=160, width=300)

		self.lbl_credit=Label(self.root, text="Total Credit\n[ 0 ]", bd=1, relief=RIDGE, bg="coral", fg="black", font=("goundy old style", 20, "bold"),image=self.creditLogo, compound="bottom", anchor="w", padx=20 )
		self.lbl_credit.place(x=1000, y=300, height=160, width=300)


		#===footer=======
		lbl_footer = Label(self.root, text="IMS-Inventory Management System | Developed By Olasunkanmi\nfor any Techical Issue Contact: 08068725871", font=("times new roman", 12), bg="#4b100a", fg="white")
		lbl_footer.pack(side=BOTTOM, fill=X)

		self.update_content()
##==============================================================================================================================

	def employee(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=employeeClass(self.new_win)


	def supplier(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=supplierClass(self.new_win)


	def category(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=categoryClass(self.new_win)


	def product(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=productClass(self.new_win)


	def sales(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=salesClass(self.new_win)


	def credit(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=creditClass(self.new_win)

	def update_content(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT * from product")
			product=cur.fetchall()
			self.lbl_product.config(text=f'Products [ {str(len(product))} ]')

			cur.execute("SELECT * from supplier")
			supplier=cur.fetchall()
			self.lbl_supplier.config(text=f'Suppliers [ {str(len(supplier))} ]')

			cur.execute("SELECT * from employee")
			employee=cur.fetchall()
			self.lbl_employee.config(text=f'Employees [ {str(len(employee))} ]')

			cur.execute("SELECT * from category")
			category=cur.fetchall()
			self.lbl_category.config(text=f'Category [ {str(len(category))} ]')

			cur.execute("SELECT * from credit")
			credit=cur.fetchall()
			self.lbl_credit.config(text=f'Credits [ {str(len(credit))} ]')
			bill=len(os.listdir('bill'))
			self.lbl_sales.config(text=f'Sales [{str(bill)}]')

			time_=time.strftime("%I:%M:%S")
			date_=time.strftime("%d-%m-%Y")
			self.lbl_clock.config(text=f"Welcome | King's Power Tech Computers\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
			self.lbl_clock.after(200, self.update_content)
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


	def logout(self):
		self.root.destroy()
		os.system("python login.py")





if __name__=="__main__":
	root=Tk()
	obj=IMS(root)
	root.mainloop()


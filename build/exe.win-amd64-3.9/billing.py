from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time 
import os
import tempfile
from credit import creditClass
class BillClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1350x700+0+0")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | Inventory Management System |   Developed By Olasunkanmi")
		self.root.config(bg="white")
		#===================================================================
		self.cart_list=[]
		self.chk_print=0

		#====title===
		self.icon_title=PhotoImage(file="images/logoo.png")
		title = Label(self.root, text="KING's POWER TECH Point Of Sales", image=self.icon_title, compound=LEFT, font=("times new roman", 30, "bold"), bg="#c0392b", fg="white", anchor="w", padx=20)
		title.place(x=0, y=0, relwidth=1, height=70)

		#===btn_logout====
		btn_logout = Button(self.root, command=self.logout, bg="yellow", fg='black', text="Logout", font=("times new roman", 13, "bold"), cursor="hand2", bd=1)
		btn_logout.place(x=1220, y=16, height=40, width=100)

		#===credit button====
		btn_credit = Button(self.root, command=self.credit, bg="#4b100a", fg='white', text="On Credit", font=("times new roman", 12, "bold"), cursor="hand2", bd=1)
		btn_credit.place(x=1050, y=16, height=40, width=120)

		#===clock and date=======
		self.lbl_clock = Label(self.root, text="Welcome to King's Power Tech Point Of Sales\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#4b100a", fg="white")
		self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

		#==Product Frames======
		self.var_search=StringVar()
		productFrame1=Frame(self.root, bd=3, relief=RIDGE, bg="white")
		productFrame1.place(x=6, y=110, width=410, height=550)

		pTitle=Label(productFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626", fg="white")
		pTitle.pack(side=TOP, fill=X)

		#==Product Search Frames======
		productFrame2=Frame(productFrame1, bd=2, relief=RIDGE, bg="white")
		productFrame2.place(x=2, y=42, width=398, height=90)

		lbl_search=Label(productFrame2, text="Search Product | By Name ", font=("times new roman", 15, "bold"), bg="white", fg="green")
		lbl_search.place(x=2, y=5)

		lbl_search=Label(productFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white")
		lbl_search.place(x=5, y=45)

		txt_search=Entry(productFrame2, textvariable=self.var_search,  font=("times new roman", 15), bg="lightyellow")
		txt_search.place(x=128, y=47, width=150, height=22)

		btn_search=Button(productFrame2, command=self.search, text="Search", font=("goudy old style",15), bg="#2196f3", fg="white", cursor="hand2")
		btn_search.place(x=285, y=45, width=100, height=25)

		btn_show_all=Button(productFrame2, command=self.show, text="Show All", font=("goudy old style",15), bg="#083531", fg="white", cursor="hand2")
		btn_show_all.place(x=285, y=10, width=100, height=25)
		
		#==Product Details Frame=====

		productFrame3=Frame(productFrame1, bd=3, relief=RIDGE)
		productFrame3.place(x=2, y=140, width=398, height=300)

		scrolly=Scrollbar(productFrame3, orient=VERTICAL)
		scrollx=Scrollbar(productFrame3, orient=HORIZONTAL)

		self.product_Table=ttk.Treeview(productFrame3, columns=("pid", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM, fill=X)
		scrolly.pack(side=RIGHT, fill=Y)
		scrollx.config(command=self.product_Table.xview)
		scrolly.config(command=self.product_Table.yview)
		self.product_Table.heading("pid", text="ID")
		self.product_Table.heading("name", text="Name")
		self.product_Table.heading("price", text="Price")
		self.product_Table.heading("qty", text="QTY")
		self.product_Table.heading("status", text="Status")
		
		self.product_Table["show"]="headings"

		self.product_Table.column("pid", width=40)
		self.product_Table.column("name", width=100)
		self.product_Table.column("price", width=90)
		self.product_Table.column("qty", width=40)
		self.product_Table.column("status", width=90)
		self.product_Table.pack(fill=BOTH, expand=1)
		self.product_Table.bind("<ButtonRelease-1>", self.get_data) # when clicked ones on table, perform whats in getdata function.
		
		lbl_note=Label(productFrame1, text="Note: 'Enter 0 Quantity to REMOVE Product from the Cart'", font=("goudy old style", 12), anchor='w', bg="white", fg="red")
		lbl_note.pack(side=BOTTOM, fill=X)
		 #display everything in the employee table inside the treeview frame.


		#===CustomerFrame=======
		self.var_cname=StringVar()
		self.var_contact=StringVar()
		CustomerFrame=Frame(self.root, bd=3, relief=RIDGE, bg="white")
		CustomerFrame.place(x=420, y=110, width=530, height=70)

		cTitle=Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg="lightgray")
		cTitle.pack(side=TOP, fill=X)

		lbl_name=Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white")
		lbl_name.place(x=5, y=35)

		txt_name=Entry(CustomerFrame, textvariable=self.var_cname,  font=("times new roman", 13), bg="lightyellow")
		txt_name.place(x=80, y=37, width=180)

		lbl_contact=Label(CustomerFrame, text="Conatct No.", font=("times new roman", 15), bg="white")
		lbl_contact.place(x=270, y=35)

		txt_contact=Entry(CustomerFrame, textvariable=self.var_contact,  font=("times new roman", 13), bg="lightyellow")
		txt_contact.place(x=380, y=35, width=140)

		#==Calculator and Cart frame=======
		Cal_Cart_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
		Cal_Cart_Frame.place(x=420, y=190, width=530, height=360)
		
		#==Calculator Frame==
		self.var_cal_input=StringVar()

		Cal_Frame=Frame(Cal_Cart_Frame, bd=9, relief=RIDGE, bg="white")
		Cal_Frame.place(x=5, y=10, width=268, height=340)

		txt_cal_input=Entry(Cal_Frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
		txt_cal_input.grid(row=0, columnspan=4)

		#==row1
		btn_7=Button(Cal_Frame, text='7', command=lambda:self.get_input(7), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_7.grid(row=1, column=0)

		btn_8=Button(Cal_Frame, text='8', command=lambda:self.get_input(8), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_8.grid(row=1, column=1)

		btn_9=Button(Cal_Frame, text='9', command=lambda:self.get_input(9), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_9.grid(row=1, column=2)

		btn_sum=Button(Cal_Frame, text='+', command=lambda:self.get_input('+'), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_sum.grid(row=1, column=3)

		#==row2
		btn_4=Button(Cal_Frame, text='4', command=lambda:self.get_input(4), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_4.grid(row=2, column=0)

		btn_5=Button(Cal_Frame, text='5', command=lambda:self.get_input(5), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_5.grid(row=2, column=1)

		btn_6=Button(Cal_Frame, text='6', command=lambda:self.get_input(6), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_6.grid(row=2, column=2)

		btn_sub=Button(Cal_Frame, text='-', command=lambda:self.get_input('-'), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_sub.grid(row=2, column=3)

		#==row3
		btn_1=Button(Cal_Frame, text='1', command=lambda:self.get_input(1), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_1.grid(row=3, column=0)

		btn_2=Button(Cal_Frame, text='2', command=lambda:self.get_input(2), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_2.grid(row=3, column=1)

		btn_3=Button(Cal_Frame, text='3', command=lambda:self.get_input(3), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_3.grid(row=3, column=2)

		btn_mul=Button(Cal_Frame, text='x', command=lambda:self.get_input('*'), font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2")
		btn_mul.grid(row=3, column=3)

		#==row4==
		btn_0=Button(Cal_Frame, text='0', command=lambda:self.get_input(0), font=('arial', 15, 'bold'), bd=5, width=4, pady=15, cursor="hand2")
		btn_0.grid(row=4, column=0)

		btn_c=Button(Cal_Frame, text='c', command=self.clear_cal, font=('arial', 15, 'bold'), bd=5, width=4, pady=15, cursor="hand2")
		btn_c.grid(row=4, column=1)

		btn_eq=Button(Cal_Frame, text='=',command=self.perform_cal, font=('arial', 15, 'bold'), bd=5, width=4, pady=15, cursor="hand2")
		btn_eq.grid(row=4, column=2)

		btn_div=Button(Cal_Frame, text='/', command=lambda:self.get_input('/'), font=('arial', 15, 'bold'), bd=5, width=4, pady=15, cursor="hand2")
		btn_div.grid(row=4, column=3)


		#==Cart Details Frame=====
		cart_Frame=Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
		cart_Frame.place(x=280, y=8, width=245, height=342)
		self.cartTitle=Label(cart_Frame, text="Total Product in Cart: [0]", font=("goudy old style", 15), bg="lightgray")
		self.cartTitle.pack(side=TOP, fill=X)


		scrolly=Scrollbar(cart_Frame, orient=VERTICAL)
		scrollx=Scrollbar(cart_Frame, orient=HORIZONTAL)

		self.CartTable=ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM, fill=X)
		scrolly.pack(side=RIGHT, fill=Y)
		scrollx.config(command=self.CartTable.xview)
		scrolly.config(command=self.CartTable.yview)
		self.CartTable.heading("pid", text="ID")
		self.CartTable.heading("name", text="Name")
		self.CartTable.heading("price", text="Price")
		self.CartTable.heading("qty", text="QTY")
		
		
		self.CartTable["show"]="headings"

		self.CartTable.column("pid", width=20)
		self.CartTable.column("name", width=90)
		self.CartTable.column("price", width=80)
		self.CartTable.column("qty", width=30)
		self.CartTable.pack(fill=BOTH, expand=1)
		self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart) # when clicked ones on table, perform whats in getdata function.

		#==Add to Cart Widgets Frame==========
		self.var_pid=StringVar()
		self.var_pname=StringVar()
		self.var_price=StringVar()
		self.var_qty=StringVar()
		self.var_stock=StringVar()
		Add_CartWidgetsFrame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
		Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

		lbl_p_name=Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white")
		lbl_p_name.place(x=5, y=5)

		txt_p_name=Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15), bg="lightyellow", state='readonly')
		txt_p_name.place(x=5, y=35, width=190, height=22)

		lbl_p_price=Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white")
		lbl_p_price.place(x=230, y=5)

		txt_p_price=Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15), bg="lightyellow", state='readonly')
		txt_p_price.place(x=230, y=35, width=150, height=22)

		lbl_p_qty=Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white")
		lbl_p_qty.place(x=390, y=5)

		txt_p_qty=Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15), bg="lightyellow")
		txt_p_qty.place(x=390, y=35, width=120, height=22)

		self.lbl_inStock=Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
		self.lbl_inStock.place(x=5, y=70)

		btn_clear_cart=Button(Add_CartWidgetsFrame, command=self.clear_cart, text="Clear", font=("times new roman", 15, "bold"), bg="lightgray", cursor="hand2")
		btn_clear_cart.place(x=180, y=70, width=150, height=30)

		btn_add_cart=Button(Add_CartWidgetsFrame, command=self.add_update_cart, text="Add | Update Cart", font=("times new roman", 15, "bold"), bg="lightgreen", cursor="hand2")
		btn_add_cart.place(x=340, y=70, width=180, height=30)

		#==Discount/Bank info frame======
		self.var_netpay=StringVar()
		self.var_pay_method=StringVar()
		self.var_bank_name=StringVar()

		
		disc_bankFrame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
		disc_bankFrame.place(x=12, y=550, width=397, height=85)

		lbl_p_netpay=Label(disc_bankFrame, text="Net Pay", font=("times new roman", 13), bg="white")
		lbl_p_netpay.place(x=5, y=5)

		txt_p_netpay=Entry(disc_bankFrame, textvariable=self.var_netpay, font=("times new roman", 13), bg="lightyellow")
		txt_p_netpay.place(x=5, y=35, width=100, height=22)

		lbl_pay_method=Label(disc_bankFrame, text="TF | Cash", font=("times new roman", 13), bg="white")
		lbl_pay_method.place(x=140, y=5)

		txt_pay_method=Entry(disc_bankFrame, textvariable=self.var_pay_method, font=("times new roman", 13), bg="lightyellow")
		txt_pay_method.place(x=140, y=35, width=100, height=22)

		lbl_pay_bank=Label(disc_bankFrame, text="Bank Name", font=("times new roman", 13), bg="white")
		lbl_pay_bank.place(x=280, y=5)

		txt_pay_bank=Entry(disc_bankFrame, textvariable=self.var_bank_name, font=("times new roman", 13), bg="lightyellow")
		txt_pay_bank.place(x=280, y=35, width=100, height=22)

		btn_add_details=Button(disc_bankFrame, command=self.adddetails, text="Add Details", font=("times new roman", 12, "bold"), bg="lightgreen", cursor="hand2")
		btn_add_details.place(x=280, y=61, width=100, height=20)


		#==Billing Area=======
		billFrame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
		billFrame.place(x=953, y=110, width=410, height=410)

		bTitle=Label(billFrame, text="Customer Bill", font=("goudy old style", 20, "bold"), bg="coral", fg="white")
		bTitle.pack(side=TOP, fill=X)

		scrolly=Scrollbar(billFrame, orient=VERTICAL)
		scrolly.pack(side=RIGHT, fill=Y)

		self.txt_bill_area=Text(billFrame, yscrollcommand=scrolly.set)
		self.txt_bill_area.pack(fill=BOTH, expand=1)
		scrolly.config(command=self.txt_bill_area.yview)

		#==Billing Buttons=========
		billMenuFrame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
		billMenuFrame.place(x=953, y=520, width=410, height=140)

		self.lbl_amnt=Label(billMenuFrame, text="Bill Amount\n[0]", font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
		self.lbl_amnt.place(x=2, y=5,width=120,height=70)

		self.lbl_disc=Label(billMenuFrame, text="Discount/Java\n[0]", font=("goudy old style", 15, "bold"), bg="#8bc34a", fg="white")
		self.lbl_disc.place(x=124, y=5,width=120,height=70)

		self.lbl_netpay=Label(billMenuFrame, text="Net Pay\n[0]", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white")
		self.lbl_netpay.place(x=246, y=5,width=145,height=70)


		btn_print=Button(billMenuFrame, command=self.print_bill, text="Print", cursor="hand2", font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
		btn_print.place(x=2, y=80,width=120,height=50)

		btn_clear_all=Button(billMenuFrame, command=self.clear_all, text="Clear All", cursor="hand2", font=("goudy old style", 15, "bold"), bg="#8bc34a", fg="white")
		btn_clear_all.place(x=124, y=80,width=120,height=50)

		btn_generate=Button(billMenuFrame, command=self.generate_bill, text="Gen/Save Bill", cursor="hand2", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white")
		btn_generate.place(x=246, y=80,width=145,height=50)

		#==footer====
		lbl_footer = Label(self.root, text="IMS-Inventory Management System | Developed By Olasunkanmi\nfor any Techical Issue Contact: 08068725871", font=("times new roman", 12), bg="#4b100a", fg="white")
		lbl_footer.pack(side=BOTTOM, fill=X)
		self.show()
		#self.bill_top()
		self.update_date_time()

	#==Credit Window========	
	def credit(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=creditClass(self.new_win)

#==========ALL FUNCTIONS FOR CALC====================================
	def get_input(self, num):
		xnum=self.var_cal_input.get()+str(num)
		self.var_cal_input.set(xnum)

	def clear_cal(self):
		self.var_cal_input.set("")

	def perform_cal(self):
		result=self.var_cal_input.get()
		self.var_cal_input.set(eval(result))

#############################################################################################################
##====FUNCTIONALITIES=====#########################################################################################################
	
	#==function for product frame======
	def show(self): #function for showing data in the treeview frame
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT pid, name, price, qty, status FROM product WHERE status='Active'")
			rows=cur.fetchall()
			self.product_Table.delete(*self.product_Table.get_children()) ##get all the rows inside the treeview table and delete them
			for row in rows:
				self.product_Table.insert('', END, values=row)    ##Display rows selected from the database in the treeview

			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


	def search(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.var_search.get()=="":
				messagebox.showerror("Error", "Please Input a Product Name", parent=self.root)
			
			else:
				cur.execute("SELECT pid, name, price, qty, status FROM product WHERE name Like '%"+self.var_search.get()+"%' AND status='Active'")
				rows=cur.fetchall()
				if len(rows)!=0:
					self.product_Table.delete(*self.product_Table.get_children()) ##get all the rows inside the treeview table and delete them
					for row in rows:
						self.product_Table.insert('', END, values=row)    ##Display rows selected from the database in the treeview
				else:
					messagebox.showerror("Error", "No record found, Try other Select options", parent=self.root)
			
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	#===========funtion for get data and ADD/UPDATE CART
	def get_data(self,ev): #function for binding selectedrow i.e wen we click on a row it shows in the entry boxes
		f=self.product_Table.focus()
		content=(self.product_Table.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_pname.set(row[1])
		self.var_price.set(row[2])
		self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
		self.var_stock.set(row[3])
		self.var_qty.set('1')


	def get_data_cart(self,ev): #function for binding selectedrow i.e wen we click on a row it shows in the entry boxes
		f=self.CartTable.focus()
		content=(self.CartTable.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_pname.set(row[1])
		self.var_price.set(row[2])
		self.var_qty.set(row[3])
		self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
		self.var_stock.set(row[4])
		


	def add_update_cart(self):
	
		if self.var_pid.get()=='':
			messagebox.showerror('Error', "Please Click on Product From the List", parent=self.root)
		elif self.var_qty.get()=='' or self.var_price.get()=='':
			messagebox.showerror('Error', "Price and Quantity required", parent=self.root)
		elif int(self.var_qty.get())>int(self.var_stock.get()):
			messagebox.showerror('Error', "Quantity greater than Available Stock", parent=self.root)	
		else:
			#price_cal=int(self.var_qty.get())*float(self.var_price.get())
			#price_cal=float(price_cal)
			price_cal=self.var_price.get()
			cart_data=[self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
			#==UpdateCart=====explanation in vid(30:00)====
			present='no'	
			index_=0 # first element in the list is always going to have 0 has its index and present will be no
			for row in self.cart_list:
				if self.var_pid.get()==row[0]: 
					present='yes'
					break
				index_+=1  #for every item we add in the catlist this represent its index in the list
			if present=='yes':
				op=messagebox.askyesno('Confirm', "The Selected Product is Already in Cart\nDo You want to UPDATE or REMOVE Product from Cart?", parent=self.root)
				if op==True:
					if self.var_qty.get()=="0":   #if option is yes and user input 0, use the index to remove it from the list
						self.cart_list.pop(index_)
					else:
						#self.cart_list[index_][2]=price_cal # 0 is not the input, do price calculation
						self.cart_list[index_][3]=self.var_qty.get() #change the quantity
			else:
				self.cart_list.append(cart_data)  #if the product is not in the cartlist before just append
			self.show_cart()
			self.bill_updates()	

		

	def bill_updates(self):
		self.bill_amnt=0	
		for row in self.cart_list:
			self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
		self.lbl_amnt.config(text=f'Bill Amount\n{str(self.bill_amnt)}')
		self.cartTitle.config(text=f"Total Product in Cart: [{str(len(self.cart_list))}]")
			
	def adddetails(self):
		try:
			self.bill_amnt2=0	
			for row in self.cart_list:
				self.bill_amnt2=self.bill_amnt2+(float(row[2])*int(row[3]))
			self.net_pay=self.var_netpay.get()
			self.discount=int(self.bill_amnt2)-int(self.net_pay)
			self.lbl_netpay.config(text=f'Net Pay\n{str(self.net_pay)}')
			self.lbl_disc.config(text=f'Discount/Java\n{str(self.discount)}')
		except:
			messagebox.showerror("Error", "Fill in Transaction Details", parent=self.root)
			
	def clear_details(self):
		self.var_netpay.set("")


	def generate_bill(self):
		if self.var_cname.get()=='' or self.var_contact.get()=='':
			messagebox.showerror("Error", f"Customer Details required", parent=self.root)
		elif len(self.cart_list)==0:
			messagebox.showerror("Error", f"Please Add Product to Cart", parent=self.root)
		elif self.var_netpay.get()=="":
			messagebox.showerror("Error", f"NetPay and Other Transaction details required", parent=self.root)

		else:
			self.bill_top()
			#==Bill middle1====
			self.bill_middle1()
			#==Bill middle2====
			self.bill_bottom()

			fp=open(f"bill/{str(self.e_receipt_no)}.txt", "w") #Open the bill folder and save the file in receipt no +txt
			fp.write(self.txt_bill_area.get('1.0', END)) #Copy everything inside the bill area.
			fp.close()
			messagebox.showinfo('Saved', "Bill Generated and Saved Successfully", parent=self.root)
			self.chk_print=1
			#messagebox.showerror("Error", "Fill in NetPay and other Transaction info")
			
	


	def bill_top(self):
		self.e_receipt_no=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
		bill_top_temp=f'''
\tKING'S POWER TECH COMPUTERS
\tPhone: 07032486154, 08135114148 
 Plot 750 Aminu Kano Cresent II, Old Banex.Abuja
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Ph no: {self.var_contact.get()}
 E-ReceiptNO. {str(self.e_receipt_no)}\t\t\tDate: {str(time.strftime("%d%m%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
		'''
		self.txt_bill_area.delete('1.0', END)
		self.txt_bill_area.insert('1.0', bill_top_temp)

	def bill_bottom(self):

		self.bill_amnt3=0	
		for row in self.cart_list:
			self.bill_amnt3=self.bill_amnt3+(float(row[2])*int(row[3]))
		self.net_pay=self.var_netpay.get()
		self.discount2=int(self.bill_amnt3)-int(self.net_pay)
		bill_bottom_temp=f'''
{str("="*46)}
 Bill Amount\t\t\t\t#{self.bill_amnt}
 Discount\t\t\t\t#{self.discount2}
 Net Pay\t\t\t\t#{self.net_pay}
 Payment Method\t\t\t\t{self.var_pay_method.get()}
 Bank Name\t\t\t\t{self.var_bank_name.get()}
 {str("="*46)}
 We Appreciate Your Patronage, THANK YOU!!!
		'''
		self.txt_bill_area.insert(END, bill_bottom_temp)


	def bill_middle1(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			for row in self.cart_list:
				pid=row[0]
				name=row[1]
				qty=int(row[4])-int(row[3])
				if int(row[3])==int(row[4]): # if quantity you are selling is equal to whats in stock ie qty in database, after selling make the product inactive which means database will not query it again because we ahve sold all left instock
					status="Inactive"
				if int(row[3])!=int(row[4]): # if quantity you are selling is less than instock then its active
					status="Active"
				price=float(row[2])*int(row[3])
				price=str(price)
				self.txt_bill_area.insert(END, "\n"+name+"\t\t\t"+row[3]+"\t#"+price)
				#====updates quantity in product Table===
				cur.execute('UPDATE product SET qty=?, status=? WHERE pid=?',(
					qty,
					status,
					pid

				))
				con.commit()
			con.close()
			self.show()
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


	def clear_cart(self):
		self.var_pid.set("")
		self.var_pname.set("")
		self.var_price.set("")
		self.var_qty.set("")
		self.lbl_inStock.config(text=f"In Stock")
		self.var_stock.set("")

	def clear_all(self):
		del self.cart_list[:]
		self.var_cname.set("")
		self.var_contact.set("")
		self.var_netpay.set("")
		self.var_pay_method.set("")
		self.var_bank_name.set("")
		self.txt_bill_area.delete("1.0", END)
		self.cartTitle.config(text=f"Total Product in Cart: [0]")
		self.lbl_amnt.config(text=f'Bill Amount\n0')
		self.lbl_netpay.config(text=f'Net Pay\n0')
		self.lbl_disc.config(text=f'Discount/Java\n0')
		self.var_search.set("")
		self.chk_print=0
		self.clear_cart()
		self.show()
		self.show_cart()

	def show_cart(self): #function for showing cart data in the treeview frame
		try:
			self.CartTable.delete(*self.CartTable.get_children()) ##get all the rows inside the treeview table and delete them
			for row in self.cart_list:
				self.CartTable.insert('', END, values=row)    ##Display rows selected from the database in the treeview
		
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

	def update_date_time(self):
		time_=time.strftime("%I:%M:%S")
		date_=time.strftime("%d-%m-%Y")
		self.lbl_clock.config(text=f"Welcome to King's Power Tech Point Of Sales\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
		self.lbl_clock.after(200, self.update_date_time)

	def print_bill(self):
		if self.chk_print==1:
			messagebox.showinfo("Print", "Please Wait... receipt Printing", parent=self.root)
			new_file=tempfile.mktemp('.txt')
			open(new_file,'w').write(self.txt_bill_area.get('1.0', END))
			os.startfile(new_file,'print')

		else:
			messagebox.showerror("Print", "Please Generate Bill", parent=self.root)

	def logout(self):
		self.root.destroy()
		os.system("python login.py")


if __name__=="__main__":
	root=Tk()
	obj=BillClass(root)
	root.mainloop()

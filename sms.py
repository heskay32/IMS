from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import africastalking
from customer import customerClass
class smsClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("700x400+220+130")
		self.root.iconbitmap("images/icon.ico")
		self.root.title("KPTC | SMS Panel |   Developed By Olasunkanmi")
		self.root.config(bg="white")
		self.root.resizable(False,False)

		self.username = "heskay32"
		self.api_key="089bbd4a7a1f1c1f9f2fc5dfb3c21493ef38b4b28d878ae635ba65fcc593ec9a"
		africastalking.initialize(self.username, self.api_key)
		self.sms=africastalking.SMS
		#self.api_key ="2525788e3c0e95ab546cd16e9139546ea83358a76006fdf83d273517c3b81b0e"
        #africastalking.initialize(self.username, self.api_key)
        #self.sms = africastalking.SMS

#========icon======================
		self.email_icon=ImageTk.PhotoImage(file="images/email2.png")
		self.customer_icon=ImageTk.PhotoImage(file="images/manage.png")

		
		#====title====
		title=Label(self.root, image=self.email_icon, compound=LEFT, text="SMS Panel", font=("goudy old style", 30, "bold"), bg="green", fg="white", anchor="w")
		title.place(x=0, y=0, relwidth=1)

		btn_customer=Button(self.root,command=self.customer, image=self.customer_icon, bd=0, bg="green", activebackground="green", cursor="hand2")
		btn_customer.place(x=632, y=2)

		desc=Label(self.root, text="**Phone Number must start with +234", font=("Calibri (Body)", 15), bg="#FFD966", fg="#262626")
		desc.place(x=0, y=66, relwidth=1)
		#=========
		self.var_choice=StringVar()
		single=Radiobutton(self.root, text="Single", value="single", variable=self.var_choice, activebackground="white", font=("times new roman", 20, "bold"), bg="white", fg="#262626", command=self.check_single_or_bulk)
		single.place(x=50, y=100)

		bulk=Radiobutton(self.root, text="Bulk", value="bulk", variable=self.var_choice, activebackground="white", font=("times new roman", 20, "bold"), bg="white", fg="#262626", command=self.check_single_or_bulk)
		bulk.place(x=200, y=100)
		self.var_choice.set("single")
		#===============
		phone=Label(self.root, text="Phone", font=("times new roman", 16), bg="white")
		phone.place(x=50, y=160)

		msg=Label(self.root, text="Message", font=("times new roman", 16), bg="white")
		msg.place(x=50, y=210)

		self.txt_phone=Entry(self.root, font=("times new roman", 14), bg="lightyellow")
		self.txt_phone.place(x=145,y=160, width=250, height=30)

		self.txt_msg=Text(self.root, font=("times new roman", 12), bg="lightyellow")
		self.txt_msg.place(x=145,y=210, width=300, height=100)

		self.btn_send=Button(self.root, command=self.send_text, text="Send", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2")
		self.btn_send.place(x=145, y=325, width=100, height=28)

		self.btn_send_to_recent=Button(self.root, command=self.send_last, text="Last customer", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2")
		self.btn_send_to_recent.place(x=255, y=325, width=150, height=28)

		self.btn_send_to_all=Button(self.root, command=self.send_all, text="All Customers", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", state=DISABLED)
		self.btn_send_to_all.place(x=255, y=355, width=150, height=28)

		self.btn_send_to_recent10=Button(self.root, command=self.send_last_10, text="Last 10", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", state=DISABLED)
		self.btn_send_to_recent10.place(x=145, y=355, width=100, height=28)


		btn_clear=Button(self.root, command=self.clear, text="Clear", font=("times new roman", 15, "bold"), bg="gray", fg="black", cursor="hand2")
		btn_clear.place(x=415, y=325, width=80, height=28)
		#self.txt_phone.set("+234")
		#self.txt_msg.config(" Thanks for coming, we will like to see you again.\nKing's Power Tech Computers ")

	def send_text(self):
		x=len(self.txt_msg.get('1.0',END))
		if self.txt_phone.get()=="" or x==1:
			messagebox.showerror("Error", "Input Phone number and Message", parent=self.root)
		else:
			recipients = [self.txt_phone.get()]
			message = str(self.txt_msg.get('1.0',END))
			try:
				response=self.sms.send(message, recipients)
				messagebox.showinfo("Success", "Message Sent", parent=self.root)
				#print(response)
			except Exception as e:
				messagebox.showerror("Connection Error", f'Error due to: {e}', parent=self.root)
	
	def send_last(self):
		list1=[]
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if len(self.txt_msg.get('1.0',END))==1:
				messagebox.showerror("Error", "Input text message")
			else:
				cur.execute("SELECT number from customer WHERE cuid=(SELECT MAX(cuid) FROM customer)")
				number=cur.fetchone()
				number=number[0]
				list1.append(number)

				recipients = list1
				message = str(self.txt_msg.get('1.0',END))

				try:
					response=self.sms.send(message, recipients)
					messagebox.showinfo("Success", "Message Sent", parent=self.root)
				except Exception as e:
					messagebox.showerror("Connection Error", f'Error due to: {e}', parent=self.root)		

		except Exception as e:
				messagebox.showerror("Error", f'Error due to: {e}', parent=self.root)

	def send_last_10(self):
		list2=[]
		list22=[]
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT number FROM customer ORDER BY cuid DESC LIMIT 10")
			numbers=cur.fetchall()
			for i in numbers:
				list2.append(i[0])
			for i in list2:
				if len(i)==14 or len(i)==15:
					list22.append(i)
			recipients = list22
			message = str(self.txt_msg.get('1.0',END))
			try:
				response=self.sms.send(message, recipients)
				messagebox.showinfo("Success", "Messages Sent", parent=self.root)
			except Exception as e:
				messagebox.showerror("Connection Error", f'Error due to: {e}', parent=self.root)		

			#print(list22)
		except Exception as e:
				messagebox.showerror("Error", f'Error due to: {e}', parent=self.root)

	def send_all(self):
		list3=[]
		list33=[]
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			cur.execute("SELECT number FROM customer")
			numbers=cur.fetchall()
			for i in numbers:
				list3.append(i[0])
			for i in list3:
				if len(i)==14 or len(i)==15:
					list33.append(i)
			recipients = list33
			message = str(self.txt_msg.get('1.0',END))
			try:
				response=self.sms.send(message, recipients)
				messagebox.showinfo("Success", "Messages Sent", parent=self.root)
			except Exception as e:
				messagebox.showerror("Connection Error", f'Error due to: {e}', parent=self.root)		

			#print(response)

		except Exception as e:
				messagebox.showerror("Error", f'Error due to: {e}', parent=self.root)


	def check_single_or_bulk(self):
		if self.var_choice.get()=="single":
			self.txt_phone.config(state='normal')
			self.btn_send.config(state=NORMAL)
			self.btn_send_to_recent.config(state=NORMAL)
			self.btn_send_to_all.config(state=DISABLED)
			self.btn_send_to_recent10.config(state=DISABLED)

		if self.var_choice.get()=="bulk":
			self.txt_phone.config(state='readonly')
			self.btn_send.config(state=DISABLED)
			self.btn_send_to_recent.config(state=DISABLED)
			self.btn_send_to_all.config(state=NORMAL)
			self.btn_send_to_recent10.config(state=NORMAL)

	def clear(self):
		self.txt_msg.delete('1.0',END)
		self.var_choice.set("single")


	def customer(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=customerClass(self.new_win)




if __name__=="__main__":
	root=Tk()
	obj=smsClass(root)
	root.mainloop()


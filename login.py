from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import smtplib
import email_pass
import time
import webbrowser

class loginSystem:
	def __init__(self,root):
		self.root=root
		self.root.title("Login System Developed By Olasunkanmi")
		self.root.geometry("1100x700+0+0")
		self.root.config(bg="white")
		self.root.iconbitmap("images/icon.ico")
		
		self.otp=''
		

		#==Login Frame======
		self.emp_id=StringVar()
		self.password=StringVar()

		login_frame=Frame(self.root, bd=0, relief=RIDGE, bg="white")
		login_frame.place(x=646, y=1, width=451, height=653)

		title=Label(login_frame, text="Login", font=("Elephant", 30, "bold"), bg="white")
		title.place(x=2, y=160, relwidth=1)

		lbl_user=Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171")
		lbl_user.place(x=50, y=230)
		txt_emp_id=Entry(login_frame, textvariable=self.emp_id, font=("times new roman", 15), bg="lightcyan")
		txt_emp_id.place(x=50, y=270,width=250)

		lbl_pass=Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171")
		lbl_pass.place(x=50, y=330)
		txt_pass=Entry(login_frame, show="*", textvariable=self.password, font=("times new roman", 15), bg="lightcyan")
		txt_pass.place(x=50, y=370,width=250)

		btn_login=Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2")
		btn_login.place(x=50, y=430, width=250, height=35)

		hr=Label(login_frame, bg="lightgray")
		hr.place(x=50, y=510, width=250, height=2)

		OR=Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold"))
		OR.place(x=150, y=500)

		btn_forget=Button(login_frame, command=self.forget_window, text="Forget Password?", font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E", cursor="hand2")
		btn_forget.place(x=100, y=535)

		btn_link1=Button(login_frame, text="Visit Our Website ||", font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E", cursor="hand2")
		btn_link1.place(x=50, y=615)

		btn_link2=Button(login_frame, command=self.open_whatsapp, text="WhatsApp ||", font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E", cursor="hand2")
		btn_link2.place(x=190, y=615)

		btn_link3=Button(login_frame, command=self.open_instagram, text="Instagram", font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E", cursor="hand2")
		btn_link3.place(x=280, y=615)

		#==footer====
		lbl_footer = Label(self.root, text="KPT Login System | Developed By Olasunkanmi\nfor any Techical Issue Contact: 08068725871", font=("times new roman", 12), bg="#4b100a", fg="white")
		lbl_footer.pack(side=BOTTOM, fill=X)

		#==Animation=========
		self.image1=PhotoImage(file="images/logo2.png")
		self.image2=PhotoImage(file="images/resize1.png")
		self.image3=PhotoImage(file="images/resize2.png")
		self.image4=PhotoImage(file="images/resize3.png")
		self.image5=PhotoImage(file="images/resize4.png")
		self.image6=PhotoImage(file="images/resize5.png")
		self.image7=PhotoImage(file="images/resize6.png")

		self.lbl_change_image=Label(self.root, bg="white")
		self.lbl_change_image.place(x=2, y=0, width=640, height=655)

		self.animate()
#======================ALL FUNCTIONS======================
		
	def animate(self):
		self.im=self.image1
		self.image1=self.image2
		self.image2=self.image3
		self.image3=self.image4
		self.image4=self.image5
		self.image5=self.image6
		self.image6=self.image7
		self.image7=self.im
		self.lbl_change_image.config(image=self.im)
		self.lbl_change_image.after(3000,self.animate)

		
	def login(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.emp_id.get()=="" or self.password.get()=="":
				messagebox.showerror("Error", "ID and Password required")
			else:
				cur.execute("SELECT utype from employee WHERE eid=? AND pass=?", (self.emp_id.get(),self.password.get()))
				user=cur.fetchone()
				if user==None:
					messagebox.showerror("Error", "Invalid ID and Password")
				else:
					#print("user")
					if user[0]=="Admin":
						self.root.destroy()
						os.system("python dashboard.py")
					else:
						self.root.destroy()
						os.system("python billing.py")
		except Exception as ex:
			messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


	

	def forget_window(self):
		con = sqlite3.connect(database=r'ims.db')
		cur = con.cursor()
		try:
			if self.emp_id.get()=="":
				messagebox.showerror("Error", "Employee ID required", parent=self.root)
			else:
				cur.execute("SELECT email from employee WHERE eid=?", (self.emp_id.get(),))
				email=cur.fetchone()
				if email==None:
					messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
				else:
					self.var_otp=StringVar()
					self.var_new_pass=StringVar()
					self.var_conf_pass=StringVar()
					#call send_email_function()
					chk=self.send_email(email[0])
					if chk=='f':
						messagebox.showerror("Error", "Connection Error\ncheck your Network.", parent=self.root)
					else:
						self.forget_win=Toplevel(self.root)
						self.forget_win.title('RESET PASSWORD')
						self.forget_win.geometry('400x350+500+100')
						self.forget_win.iconbitmap("images/icon.ico")
						self.forget_win.focus_force()

						title=Label(self.forget_win, text='Reset Password', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white")
						title.pack(side=TOP, fill=X)
						lbl_reset=Label(self.forget_win, text='Enter OTP Sent to Your Registered Email', font=('times new roman', 15))
						lbl_reset.place(x=20, y=60)

						txt_reset=Entry(self.forget_win, textvariable=self.var_otp, font=('times new roman', 15), bg="lightcyan")
						txt_reset.place(x=20, y=100, width=250, height=30)
						self.btn_reset=Button(self.forget_win, command=self.validate_otp, text="SUBMIT", font=('times new roman', 15), bg="lightblue")
						self.btn_reset.place(x=280, y=100, width=100, height=30)

						lbl_new_pass=Label(self.forget_win, text='New Password', font=('times new roman', 15))
						lbl_new_pass.place(x=20, y=160)
						txt_new_pass=Entry(self.forget_win, textvariable=self.var_new_pass, font=('times new roman', 15), bg="lightcyan")
						txt_new_pass.place(x=20, y=190, width=250, height=30)

						lbl_c_pass=Label(self.forget_win, text='Confirm New Password', font=('times new roman', 15))
						lbl_c_pass.place(x=20, y=225)
						txt_c_pass=Entry(self.forget_win, textvariable=self.var_conf_pass, font=('times new roman', 15), bg="lightcyan")
						txt_c_pass.place(x=20, y=255, width=250, height=30)

						self.btn_update=Button(self.forget_win, command=self.update_password, text="Change Password", state=DISABLED, font=('times new roman', 15), bg="lightblue")
						self.btn_update.place(x=115, y=300, width=155, height=30)
		except Exception as ex:
			messagebox.showerror("Connection Error", f"Error due to : {str(ex)}", parent=self.root)
	
	def update_password(self):
		if self.var_new_pass.get()=="" or self.var_conf_pass=="":
			messagebox.showerror("Error", "New Password required", parent=self.forget_win)
		elif self.var_new_pass.get()!=self.var_conf_pass.get():
			messagebox.showerror("Error", "New Password and Confirm Password must be thesame", parent=self.forget_win)
		else:
			con = sqlite3.connect(database=r'ims.db')
			cur = con.cursor()
			try:
				cur.execute("UPDATE employee SET pass=? WHERE eid=?", (self.var_new_pass.get(), self.emp_id.get()))
				con.commit()
				messagebox.showinfo("Success", "Password Updated Successfully", parent=self.forget_win)
				self.forget_win.destroy()


			except Exception as ex:
				messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.forget_win)


	def validate_otp(self):
		if int(self.otp)==int(self.var_otp.get()):
			self.btn_update.config(state=NORMAL)
			self.btn_reset.config(state=DISABLED)
		else:
			messagebox.showerror("Error", "Invalid OTP\nTry again", parent=self.forget_win)

	def send_email(self,to_):
		s=smtplib.SMTP('smtp.gmail.com',587) #connect to gmail server(host), 587 is the port
		s.starttls() #tells gmail to turn an existing insecure connection into a secure one
		email_=email_pass.email_	
		pass_=email_pass.pass_
		s.login(email_,pass_)

		self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
		
		subj="KING's POWER TECH COMPUTERS IMS-Reset Password OTP"
		msg=f"Dear Sir/Maam,\n\nYour Reset OTP is {str(self.otp)}\n\nWith Regards,\nKPT-Computers IMS Team"
		msg="Subject:{}\n\n{}".format(subj,msg)
		s.sendmail(email_,to_,msg)
		chk=s.ehlo()#to check there is a connection with other server
		if chk[0]==250:
			return 's' #return success, meaning there is connection
		else:
			return 'f'


	def open_instagram(self):
		webbrowser.open("https://www.instagram.com/deexanalytics/")

	def open_whatsapp(self):
		webbrowser.open("https://wa.link/y810pe")
		
	

root=Tk()
obj=loginSystem(root)
root.mainloop()

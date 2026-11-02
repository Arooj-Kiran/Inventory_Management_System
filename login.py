from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import messagebox
import sqlite3
import os

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed By Arooj")
        self.root.geometry("1200x700+0+0")
        self.root.config(bg="#fafafa")

        # ====== Images ======
        self.left_image = ImageTk.PhotoImage(file="img/pin.login.jpg")  # <-- change path if needed
        self.lbl_left_image = Label(self.root, image=self.left_image, bg="white")
        self.lbl_left_image.place(x=67, y=120, width=600, height=400)

        # ====== Login Frame ======
        self.employee_id = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=750, y=90, width=350, height=400)

        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white").place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=100)
        
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=140, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=200)
        
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)

        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15),
                           bg="#0f4d7b", fg="white", activebackground="#0f4d7b", activeforeground="white").place(x=50, y=300, width=250, height=35)



# ============== FUNCTIONS =============       

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:

                cur.execute("SELECT * FROM employee WHERE EmpID=? AND Password=?", (self.employee_id.get(), self.password.get()))
                user= cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid UserName / Password",parent=self.root)
                else:
                    if user[8] == "Admin":   # 8th column is UserType (based on your employee table structure)
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()

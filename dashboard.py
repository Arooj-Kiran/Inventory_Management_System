from tkinter import*
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
import os
import time

BG_COLOR = "#0f4d7b"  
TITLE_COLOR = "#ffffff"
HEADER_COLOR = "#1f6e8c"

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Developed By Arooj")
        self.root.state('zoomed') 
        self.root.config(bg="white")

        #=====title====

        title_frame = tk.Frame(self.root, bd=5, relief=tk.RIDGE, bg=HEADER_COLOR)
        title_frame.place(x=0, y=0, relwidth=1, height=70)

        title_label = tk.Label(
            title_frame,
            text="Inventory Management System",
            compound=tk.LEFT,
            font=("times new roman", 30, "bold"),
            bg=HEADER_COLOR,
            fg=TITLE_COLOR,
            anchor="w",
            padx=20
        )
        title_label.pack(fill=tk.BOTH, expand=True)


        #====btn logout====
        btn_logout=tk.Button(
            title_frame,
            text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow",
            command=self.logout,
            cursor="hand2"
            ).place(x=1400,y=10,height=40,width=150)
        

        #====clock====
        self.lbl_clock=Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD/MM/YYYY \t\t Time: HH:MM:SS",
            font=("goudy old style", 15),
            bg="#4d636d",
            fg="white"
            )
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)


        #====Left Menu====
        self.MenuLogo=Image.open("img/p_inventory.png")
        self.MenuLogo=self.MenuLogo.resize((250,250))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=250,height=730)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        lbl_menu=Label(
            LeftMenu,
            text="Menu",
            font=("times new roman", 20),
            bg="#009688",
            ).pack(side=TOP,fill=X)
        
        btn_employee=Button(
            LeftMenu,
            text="⫸  Employee",
            command=self.employee,
            font=("times new roman", 20,"bold"),
            bg="white",
            bd=3,
            anchor="w",
            padx=5,
            cursor="hand2"
            ).pack(side=TOP,fill=X)
        
        btn_supplier=Button(
            LeftMenu,
            text="⫸  Supplie",
            font=("times new roman", 20,"bold"),
            bg="white",
            bd=3,
            command=self.supplier,
            anchor="w",
            padx=5,
            cursor="hand2"
            ).pack(side=TOP,fill=X)
        
        btn_category=Button(
            LeftMenu,
            text="⫸  Category",
            font=("times new roman", 20,"bold"),
            bg="white",
            bd=3,
            command=self.category,
            anchor="w",
            padx=5,
            cursor="hand2"
            ).pack(side=TOP,fill=X)
        
        btn_product=Button(
            LeftMenu,
            text="⫸  Products",
            font=("times new roman", 20,"bold"),
            bg="white",
            bd=3,
            command=self.product,
            cursor="hand2",
            anchor="w",
            padx=5
            ).pack(side=TOP,fill=X)
        
        btn_sales=Button(
            LeftMenu,
            text="⫸  Sales",
            font=("times new roman", 20,"bold"),
            bg="white",
            bd=3,
            anchor="w",
            command=self.sales,
            padx=5,
            cursor="hand2"
            ).pack(side=TOP,fill=X)
        
        btn_exit=Button(
            LeftMenu,
            text="⫸  Exit",
            font=("times new roman", 20,"bold"),
            bg="white",
            bd=3,
            anchor="w", 
            padx=5,
            cursor="hand2"
            ).pack(side=TOP,fill=X)
        
        #====Content====
#1. lbl_employee
        self.lbl_employee=Label(self.root,
            text="Total Employee\n[ 0 ]",
            bg="#33bbf9",
            fg="white",
            bd=5,
            relief=RIDGE,
            font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)
#2. lbl_supplier
        self.lbl_supplier=Label(self.root,
            text="Total Supplier\n[ 0 ]",
            bg="#ff5722",
            fg="white",
            bd=5,
            relief=RIDGE,
            font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)
#3. lbl_category
        self.lbl_category=Label(self.root,
            text="Total Category\n[ 0 ]",
            bg="#009688",
            fg="white",
            bd=5,
            relief=RIDGE,
            font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)
#4. lbl_product
        self.lbl_product=Label(self.root,
            text="Total Product\n[ 0 ]",
            bg="#607d8b",
            fg="white",
            bd=5,
            relief=RIDGE,
            font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)
#5. lbl_sales
        self.lbl_sales=Label(self.root,
            text="Total Sales\n[ 0 ]",
            bg="#ffc107",
            fg="white",
            bd=5,
            relief=RIDGE,
            font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)
        

        #====Footer====
        lbl_footer=Label(self.root,
            text="IMS-Inventory Management System | Developed By Arooj\nFor any Technical I" \
            "Issue Contact: +92 308 xxxxxxx",
            font=("goudy old style",12),
            bg="#4d636d",
            fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
        
#=============================================================================

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
        
    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product= cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n[ {str(len(product))} ]")

            cur.execute("select * from supplier")
            supplier= cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[ {str(len(supplier))} ]")

            cur.execute("select * from category")
            category= cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {str(len(category))} ]")

            cur.execute("select * from employee")
            employee= cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {str(len(employee))} ]")
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales\n [{str(bill)}]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)} \t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)   #ye ftn hr 2 mili sec bd chalta rhy ga

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def logout(self):
        self.root.destroy()        
        os.system("python login.py")


if __name__=="__main__":
    root = Tk()
    obj = IMS(root) 
    root.mainloop()
    
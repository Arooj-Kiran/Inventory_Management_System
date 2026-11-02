from tkinter import*
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
import sqlite3
import datetime
import time
import os
import tempfile


BG_COLOR = "#0f4d7b"  
TITLE_COLOR = "#ffffff"
HEADER_COLOR = "#1f6e8c"

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Developed By Arooj")
        self.root.state('zoomed') 
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0

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
            cursor="hand2",
            command=self.logout
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

            # SIDE .1        
# ============= Product Frame =======

        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="All Products",font=("times new roman",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
# Product Search Frame
        self.var_search=StringVar()

        ProductFrame2=Frame(ProductFrame1,bd=4,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_searchPro=Label(ProductFrame2,text="Search Product | By Name",font=("goudy old style",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_namePro=Label(ProductFrame2,text="Product Name",font=("goudy old style",15,"bold"),bg="white").place(x=2,y=45)

        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("goudy old style",15),bg="lightyellow").place(x=145,y=50,width=150,height=22)

        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style", 15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=300,y=47,height=27,width=85)

        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style", 13,"bold"),bg="#083531",fg="white",cursor="hand2").place(x=300,y=10,height=25,width=85)
# Product Detail Frame
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140,width=398 , height=375)

        scroll_y = Scrollbar(ProductFrame3, orient=VERTICAL)
        scroll_x = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        # Treeview (Table) setup
        self.product_Table = ttk.Treeview(
            ProductFrame3,
            columns=("pid", "name", "price", "qty","status"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set)
        
# Configure scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.product_Table.xview)
        scroll_y.config(command=self.product_Table.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("goudy old style",11, "bold"))

        self.product_Table.heading("pid", text="P ID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")

        self.product_Table['show'] = 'headings'

        # Set column widths (approximate sizes)
        self.product_Table.column("pid", width=50,anchor="center")
        self.product_Table.column("name", width=95,anchor="center")
        self.product_Table.column("price", width=95,anchor="center")
        self.product_Table.column("qty", width=50,anchor="center")
        self.product_Table.column("status", width=95,anchor="center")

        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)


        # SIDE .2
# =========== Customer Frame ===========
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("times new roman",15),bg="lightgray").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("goudy old style",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("goudy old style",13),bg="lightyellow").place(x=80,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("goudy old style",15),bg="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("goudy old style",13),bg="lightyellow").place(x=380,y=35,width=140)
# ================ Cal_Cart_Frame ==================
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)
# ================  Calculator Frame ================ 
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,"bold"),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,"bold"),command=lambda:self.get_input(7),bd=5,width=4,pady=11,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,"bold"),command=lambda:self.get_input(8),bd=5,width=4,pady=11,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,"bold"),command=lambda:self.get_input(9),bd=5,width=4,pady=11,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,"bold"),command=lambda:self.get_input('+'),bd=5,width=4,pady=11,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=('arial',15,"bold"),command=lambda:self.get_input(4),bd=5,width=4,pady=11,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,"bold"),command=lambda:self.get_input(5),bd=5,width=4,pady=11,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,"bold"),command=lambda:self.get_input(6),bd=5,width=4,pady=11,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,"bold"),command=lambda:self.get_input('-'),bd=5,width=4,pady=11,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,"bold"),command=lambda:self.get_input(1),bd=5,width=4,pady=11,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,"bold"),command=lambda:self.get_input(2),bd=5,width=4,pady=11,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,"bold"),command=lambda:self.get_input(3),bd=5,width=4,pady=11,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='x',font=('arial',15,"bold"),command=lambda:self.get_input('*'),bd=5,width=4,pady=11,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,"bold"),command=lambda:self.get_input(0),bd=5,width=4,pady=12,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='C',font=('arial',15,"bold"),command=self.clear_cal,bd=5,width=4,pady=12,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,"bold"),command=self.perform_cal,bd=5,width=4,pady=12,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,"bold"),command=lambda:self.get_input('/'),bd=5,width=4,pady=12,cursor="hand2").grid(row=4,column=3)


# ================  Cart Frame ================ 
        cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=280, y=8,width=245 , height=342)
        self.cartTitle=Label(cart_Frame,text="Cart \t Total Product: [0]",font=("times new roman",15,"bold"),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)


        scroll_y = Scrollbar(cart_Frame, orient=VERTICAL)
        scroll_x = Scrollbar(cart_Frame, orient=HORIZONTAL)

        # Treeview (Table) setup
        self.CartTable = ttk.Treeview(
            cart_Frame,
            columns=("pid", "name", "price", "qty"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set)
        
#  ================ Configure scrollbars ================ 
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.CartTable.xview)
        scroll_y.config(command=self.CartTable.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("goudy old style",11, "bold"))

        self.CartTable.heading("pid", text="P.ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable['show'] = 'headings'


        # Set column widths (approximate sizes)
        self.CartTable.column("pid", width=40,anchor="center")
        self.CartTable.column("name", width=85,anchor="center")
        self.CartTable.column("price", width=80,anchor="center")
        self.CartTable.column("qty", width=40,anchor="center")
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

# ========== Add Cart Widgets Frame =========== "bottom side"
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("goudy old style",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=215,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow",state='readonly').place(x=215,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=390,y=35,width=130,height=22)

        self.lbl_instock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="light gray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)

# ================ Billing Area  ================
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=410,height=410)
        BTitle=Label(billFrame,text="Customer Bill Area",font=("times new roman",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        scroll_y=Scrollbar(billFrame,orient=VERTICAL)
        scroll_y.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scroll_y.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scroll_y.config(command=self.txt_bill_area.yview)

# ================ Billing Buttons  ================
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=410,height=140)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount \n [0]",font=("goudy old style",15,"bold"),bd=2,bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=130,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount \n [5%]",font=("goudy old style",15,"bold"),bd=2,bg="#048f27",fg="white")
        self.lbl_discount.place(x=135,y=5,width=130,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay \n [0]",font=("goudy old style",15,"bold"),bd=2,bg="gray",fg="white")
        self.lbl_net_pay.place(x=270,y=5,width=130,height=70)

        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",15,"bold"),cursor="hand2",bd=2,bg="#de7621")
        btn_print.place(x=2,y=80,width=130,height=55)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,font=("goudy old style",15,"bold"),cursor="hand2",bd=2,bg="#082e30",fg="white")
        btn_clear_all.place(x=135,y=80,width=130,height=55)

        btn_generate=Button(billMenuFrame,text="Generate \n Save Bill",command=self.generate_bill,font=("goudy old style",15,"bold"),cursor="hand2",bd=2,bg="#830B5F",fg="white")
        btn_generate.place(x=270,y=80,width=130,height=55)

        #=============== Footer ==========
        footer=Label(self.root,text="IMS-Inventory Management System | Developed By Arooj \n For Any Technical Issue Contect: +92 308 xxxxxxx",
            font=("goudy old style",12),
            bg="#4d636d",
            fg="white").pack(side=BOTTOM,fill=X)
        
        self.show()
        # self.bill_top()
        self.update_date_time()

# ================ All Functions  ================ 
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    def clear_cal(self):
        self.var_cal_input.set('')
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

#SHOW FUNCTION============
    def show(self):
    
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, price, qty,status FROM product where status= 'Active'")
            rows = cur.fetchall() 
            self.product_Table.delete(*self.product_Table.get_children())
            
            if len(rows) != 0:
                for row in rows:
                    self.product_Table.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)


# SEARCH FUNCTION =====================================
    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
           
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                # The query uses placeholders and string formatting to dynamically select the search column.
                # This allows searching by name, email, contact, etc.
                cur.execute("select pid, name, price, qty,status from product where name LIKE '%" + self.var_search.get() + "%' and status= 'Active'")
                rows = cur.fetchall()
                
                if len(rows) != 0:
                    # Clear previous data from the Treeview
                    self.product_Table.delete(*self.product_Table.get_children())
                    # Insert search results
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


#=================== GET FUNCTION================
    def get_data(self, ev):
        f = self.product_Table.focus()
        content = self.product_Table.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

#=================== GET Data Cart FUNCTION================
    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        

#================= Add Update Cart FUNCTION================
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please Select Product from the List",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)

        else:
            # price_cal=int(self.var_qty.get())*float(self.var_price.get())
            # price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]




#========== Update cart ===========
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present \nDo you want to Update / Remove from Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2]=price_cal                   #index of price
                        self.cart_list[index_][3]=self.var_qty.get()            #index of qty
            else:            
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()


#============= Bill Update Fuction =========

    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:

            self.bill_amnt= self.bill_amnt + (float(row[2])*int(row[3]))           # 2 pe price 3 pe qty
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")
        

#=========== Show cart Function ===============
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)


#============= Generate Bill ==============
    def generate_bill(self):
        if self.var_cname.get()==''or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are requried",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add Product to the Cart !!",parent=self.root)

        else:
            self.bill_top()    # Bill Top 
            self.bill_middle()  # Bill Middle 
            self.bill_bottom()  # Bill Bottom 


            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been Generated/Saved in Backend",parent=self.root)
            self.chk_print=1
            
#============== Bill Top Function ==============
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tArooj-Inventory
\t Phone No. +92 308 xxxxxxx , Faisalabad
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 {'Product':<12}{'Qty':<6}{'Price':<13}{'Total':<20}
{str("-"*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)    

#============== Bill  Bottom Function ============== 
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)


#============== Bill  Middle Function ============== 

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1][:12]  # limit length
                price = float(row[2])
                qty_purchased = int(row[3])
                current_stock = int(row[4])

                # new stock after purchase
                qty_left = current_stock - qty_purchased
                if qty_purchased==current_stock:
                    status='Inactive'
                if qty_purchased!=current_stock:
                    status='Active'

                total = price * qty_purchased

                # --- formatted line for bill area ---
                line = f" {name:<12}{qty_purchased:<6}Rs.{price:<9.0f}Rs.{total:<10.0f}"
                self.txt_bill_area.insert(END, f"\n{line}")

                # --- update stock in DB ---
                cur.execute(
                    'UPDATE product SET qty=?, status=? WHERE pid=?',
                    (qty_left, status, pid)
                )
                con.commit()

            con.close()
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

            

# =============== Clear Cart ===================
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

# =============== Clear All ===================
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0

# =============== Date Time ===================
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)} \t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)   #ye ftn hr 2 mili sec bd chalta rhy ga
# =============== Print Bill ===================
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please Generate Bill, to print the receipt",parent=self.root)

# =============== Logout ===================
    def logout(self):
        self.root.destroy()        
        os.system("python login.py")


if __name__=="__main__":
    root = Tk()
    obj = BillClass(root) 
    root.mainloop()
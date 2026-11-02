from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3


BG_COLOR = "#0f4d7b"  
TITLE_COLOR = "#ffffff"
HEADER_COLOR = "#1f6e8c"

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Developed By Arooj")
        self.root.geometry("800x500+220+130") 
        self.root.config(bg="#cfecf7")
        self.root.focus_force()


        # ===== Variables (for storing input data) ======

        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        
        #=====SEARCH FRAME======
        SearchFrame=LabelFrame(self.root,
            text="Search Emploee",
            bg="#cfecf7",
            font=("goudy old style",12,"bold"),
            bd=2,
            relief=RIDGE,)
        
        SearchFrame.place(x=100,y=20,width=600,height=70)


        #=====OPTIONS======
        lbl_search=Label(SearchFrame,
            text="Search By Invoice No.",
            font=("goudy old style",14),
            bg="#cfecf7")
        
        lbl_search.place(x=10,y=10)
        

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10,width=200)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

#======title=====
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 15, "bold"), bg="#0f4d7d", fg="white")
        title.place(x=50, y=100, width=700)


#=======content=======

        # ROW 1 =========================================
        lbl_supplier_invoice = Label(self.root, text="Invoice No.", font=("goudy old style", 15), bg="#cfecf7").place(x=50, y=150)
        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=150,width=180)

        # ROW 2 =======================================
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="#cfecf7").place(x=50, y=190)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=190,width=180)

        # ROW 3 =========================================
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="#cfecf7").place(x=50, y=230)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=230,width=180)
        

        # ROW 3 =========================================
        lbl_desc = Label(self.root, text="Description ", font=("goudy old style", 15), bg="#cfecf7").place(x=50, y=270)
        self.txt_desc = Text(self.root,  font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=152, y=270,width=300,height=60)
        
       
# ==== Action Buttons ======
        btn_add =Button(self.root, text="Save",command=self.add, font=("goudy old style", 15),bg="#2196f3",fg="white", cursor="hand2")
        btn_add.place(x=620,y=150,width=110,height=28)

        btn_update =Button(self.root, text="Update",command=self.update, font=("goudy old style", 15),bg="#4caf50",fg="white", cursor="hand2")
        btn_update.place(x=620,y=200,width=110,height=28)

        btn_delete =Button(self.root, text="Delete",command=self.delete, font=("goudy old style", 15),bg="#f44336",fg="white", cursor="hand2")
        btn_delete.place(x=620,y=250,width=110,height=28)

        btn_clear =Button(self.root, text="Clear",command=self.clear, font=("goudy old style", 15),bg="#607d8b",fg="white", cursor="hand2")
        btn_clear.place(x=620,y=300,width=110,height=28)


# === Employee Data Table (Bottom Section) ===
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scroll_y = Scrollbar(emp_frame, orient=VERTICAL)
        scroll_x = Scrollbar(emp_frame, orient=HORIZONTAL)

        # Treeview (Table) setup
        self.supplierTable = ttk.Treeview(
            emp_frame,
            columns=("invoice", "name", "contact", "desc"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set)
        
# Configure scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.supplierTable.xview)
        scroll_y.config(command=self.supplierTable.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("goudy old style",11, "bold"))

        self.supplierTable.heading("invoice", text="Invoice")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
      
        self.supplierTable['show'] = 'headings'


        # Set column widths (approximate sizes)
        self.supplierTable.column("invoice", width=90,anchor="center")
        self.supplierTable.column("name", width=100,anchor="center")
        self.supplierTable.column("contact", width=100,anchor="center")
        self.supplierTable.column("desc", width=100,anchor="center")
   
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()  
  #==============================================================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice no. already assigned, Try different",parent=self.root)
                else:
                    cur.execute("Insert into supplier(invoice, name, contact,desc) values(?,?,?,?)",(
                                self.var_sup_invoice.get(),
                                self.var_name.get(),
                                self.var_contact.get(),
                                self.txt_desc.get('1.0',END),

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Addedd Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)

#SHOW FUNCTION============
    def show(self):
    
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall() 
            self.supplierTable.delete(*self.supplierTable.get_children())
            
            if len(rows) != 0:
                for row in rows:
                    self.supplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)

#GET FUNCTION================
    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content['values']
        if row:
            self.var_sup_invoice.set(row[0])  
            self.var_name.set(row[1])      
            self.var_contact.set(row[2])    
            self.txt_desc.delete('1.0', END)
            self.txt_desc.insert('1.0', row[3])
            
# UPDATE =========================
    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be Required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("Update supplier SET name=?, contact=?, desc=? where invoice=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END), 
                        self.var_sup_invoice.get() 
                    ))
                
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                    self.show() 
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        


# DELETE ===========================
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "invoice no. is required", parent=self.root)
                return
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice no.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to Delete this Supplier?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier record deleted successfully", parent=self.root)
                        
                        self.clear()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# CLEAR FUNCTION =====================
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")        
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show()



# SEARCH FUNCTION =====================================
    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
            else:
                # The query uses placeholders and string formatting to dynamically select the search column.
                # This allows searching by name, email, contact, etc.
                cur.execute("select * from supplier where invoice=? " ,( self.var_searchtxt.get(),))
                row = cur.fetchone()
                
                if row != None:
                    # Clear previous data from the Treeview
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    
        

if __name__=="__main__":
    root = Tk()
    obj = supplierClass(root) 
    root.mainloop()


    

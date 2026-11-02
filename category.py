from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3


BG_COLOR = "#0f4d7b"  
TITLE_COLOR = "#ffffff"
HEADER_COLOR = "#1f6e8c"

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Developed By Arooj")
        self.root.geometry("1100x500+220+130") 
        self.root.config(bg="#cfecf7")
        self.root.focus_force()

#========= Variables=========
        self.var_cat_id = StringVar()     #User ne jo type kiya → variable me store ho jata
        self.var_name = StringVar()       #Variable ko update karoge → Entry/Label me automatically reflect ho jata
        

#======== TITLE ==============
        lbl_title = Label(self.root, text="Manage Product Category", font=("times new roman", 30), bg="#0f4d7d", fg="white",bd=3,relief=RIDGE)
        lbl_title.pack(side=TOP,fill=X,padx=10,pady=20)
  

        lbl_name = Label(self.root, text="Enter Category Name", font=("times new roman", 30), bg="#cfecf7")
        lbl_name.place(x=50,y=100)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="light yellow")
        txt_name.place(x=50, y=170, width=300)

#========== BUTTON =============
        btn_add = Button(self.root, text="Add", command=self.add,  font=("goudy old style", 15, "bold"),bg="green", fg="white", cursor="hand2")
        btn_add.place(x=360, y=170, width=150, height=30)

        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("goudy old style", 15, "bold"),bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=520, y=170, width=150, height=30)


#========= Treeview Configuration =============     #Category list dikhane ke liye frame

        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=100)

        # Scrollbars
        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("goudy old style",11, "bold"))     #Treeview ke headings ka font set.
        
        self.CategoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.CategoryTable.yview)
        scrollx.config(command=self.CategoryTable.xview)

        # Column Headings
        self.CategoryTable.heading("cid", text="Category ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"] = "headings"
        
        # Column Widths
        self.CategoryTable.column("cid", width=30,anchor="center")
        self.CategoryTable.column("name", width=150,anchor="center")
        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)



#========= IMAGES =========
        self.im1 = Image.open("img/cat3.jpg") 
        self.im1 = self.im1.resize((500, 250), Image.LANCZOS)
        self.im1 = ImageTk.PhotoImage(self.im1)
        self.lbl_im1 =Label(self.root, image=self.im1, bd=2, relief=RAISED)
        self.lbl_im1.place(x=50, y=220)
  
        self.im2 = Image.open("img/cat2.png") 
        self.im2 = self.im2.resize((500, 250), Image.LANCZOS)
        self.im2 = ImageTk.PhotoImage(self.im2)
        self.lbl_im2 =Label(self.root, image=self.im2, bd=2, relief=RAISED)
        self.lbl_im2.place(x=580, y=220)
        self.show()

#  ========= FUNCTIONS ===========
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))  #Database me check ki same name hai ya nahi
                row=cur.fetchone()
                if row!=None:    #category already exists.
                    messagebox.showerror("Error","Category already present, Try different",parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category Addedd Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)

#SHOW FUNCTION============
    def show(self):
    
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall() 
            self.CategoryTable.delete(*self.CategoryTable.get_children())    #Table ko clean kar raha
            
            
            for row in rows:
                self.CategoryTable.insert('', END, values=row)      #Saare rows table me add.

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)

#GET FUNCTION================
    def get_data(self, ev):               #Table me selected row ko entry boxes me load karta hai
        f = self.CategoryTable.focus()           #Selected row ka data milta hai
        content = self.CategoryTable.item(f)
        row = content['values']
        if row:
            self.var_cat_id.set(row[0])  
            self.var_name.set(row[1]) 

# DELETE ===========================
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please select a Category from the list", parent=self.root)
                return
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                
                if row == None:
                    messagebox.showerror("Error", "Error, Please try again.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to Delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category record deleted successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name("")
                        # self.clear()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

                                    




if __name__=="__main__":
    root = Tk()
    obj = categoryClass(root) 
    root.mainloop()
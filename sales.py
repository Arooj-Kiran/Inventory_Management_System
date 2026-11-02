from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

BG_COLOR = "#0f4d7b"  
TITLE_COLOR = "#ffffff"
HEADER_COLOR = "#1f6e8c"

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Developed By Arooj")
        self.root.geometry("1100x500+220+130") 
        self.root.config(bg="#cfecf7")
        self.root.focus_force()

#==== Variable =====
        self.bill_list=[]
        self.var_invoice=StringVar()


#===== TITLE ========
        lbl_title = Label(self.root, text="View Customer Bill", font=("times new roman", 30), bg="#0f4d7d", fg="white",bd=3,relief=RIDGE)
        lbl_title.pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root, text="Invoice No.", font=("goudy old style", 15),bg="#cfecf7").place(x=50,y=100)
        txt_invoice=Entry(self.root, textvariable=self.var_invoice, font=("goudy old style", 15),bg="lightyellow").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)

        btn_clear =Button(self.root, text="Clear",command=self.clear, font=("goudy old style", 15),bg="lightgrey", cursor="hand2")
        btn_clear.place(x=490,y=100,width=120,height=28)

#======== Sales_Frame ======
        sales_Frame=LabelFrame(self.root,
            bg="#cfecf7",
            font=("goudy old style",12,"bold"),
            bd=3,
            relief=RIDGE,)
        sales_Frame.place(x=50,y=140,width=200,height=330)
        # scroll bar
        scroll_y = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("goudy old style",15),bg="#cfecf7",yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)

#========= Billing Area =========
        bill_Frame=LabelFrame(self.root,
            bg="#cfecf7",
            bd=3,
            relief=RIDGE,)
        bill_Frame.place(x=280,y=140,width=410,height=330)
        # title
        lbl_title2 = Label(bill_Frame, text="Customer Bill Area", font=("times new roman", 20), bg="#d9a853")
        lbl_title2.pack(side=TOP,fill=X)
        # scroll bar
        scroll_y2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="lightyellow",yscrollcommand=scroll_y2.set)
        scroll_y2.pack(side=RIGHT,fill=Y)
        scroll_y2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

#====== Images =========
        self.bill_photo=Image.open("img/bill2.jpg")
        self.bill_photo=self.bill_photo.resize((370,330))
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)
        lbl_image=Label(self.root,image=self.bill_photo,bd=0)        
        lbl_image.place(x=710,y=140)

        self.show()
# =======================================================================================

    # billing file
    def show(self):  
        del self.bill_list[:]  
        self.Sales_List.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])
    
    # to show data from file
    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        print(file_name)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice No. ",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)


if __name__=="__main__":
    
    root = Tk()
    obj = salesClass(root) 
    root.mainloop()
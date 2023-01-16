
from tkinter import *
from tkinter import messagebox
import random
import sqlite3

#Email is made as username
count = 0 #to quit other window incase 


#LOGIN AND REGISTER ------------------------------------------------------------------------------------------------------------------------

def create_acc():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()

    c.execute("INSERT INTO allaccounts VALUES (:name, :email,:pass, :rc)",
        {
            'name': name.get(),
            'email': em_reg.get(),
            'pass': ps_reg.get(),
            'rc': rc_reg.get()

        })
    messagebox.showinfo("", "Account Created")
    messagebox.showinfo("", "Please keep the registaration code safely\nYour regestaration code = " + rc_reg.get())
    cust_login()
    conn.commit()
    conn.close()

def auth_reg():
    ex_em,ex_rc = 0,0
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    l = len(rc_reg.get())
    auth_rc_reg = rc_reg.get()
    auth_em_reg = em_reg.get()
    auth_ps_reg = ps_reg.get()
    auth_cps_reg = cps_reg.get()
    nl = name.get() #name 
    nl_l = nl.find(' ') #length

    fad=auth_em_reg.find("@")

    c.execute("SELECT email,pass FROM allaccounts")
    all_accounts = c.fetchall()
    for accounts in all_accounts:
        if accounts[0] == auth_em_reg:
            ex_em=1
            break
        elif accounts[1] == auth_rc_reg:
            ex_rc=1
            break


    if nl_l == -1:
        messagebox.showerror("Full name required") 
    elif len(auth_ps_reg) <=8:
        messagebox.showerror("", "Password must be of more than 8 characters")
    elif auth_ps_reg != auth_cps_reg:
        messagebox.showerror("", "password doesn't match")
    elif ex_rc ==1:
        messagebox.showerror("","Account with registration number exists")
    elif ex_em == 1:
        messagebox.showerror("", "Account with this email exists")
    else:
        create_acc()
        

    conn.commit()
    conn.close()

def change_pass():
    global change_pass_scr,new_pass_entry
    change_pass_scr = Toplevel()
    change_pass_scr.geometry("300x150+600+250")
    change_pass_scr.title("Change Password")

    Label(change_pass_scr, text="Enter your new password", font=("Open Sans", 12, "bold")).pack()
    new_pass_entry = Entry(change_pass_scr, width=30, border=0, font=("Open Sans", 12))
    new_pass_entry.pack()

    submit_btn = Button(change_pass_scr, text="Submit", font=("Open Sans", 12, "bold"), width=20, border=0, bg="#14D8ED", fg="#fff")
    submit_btn.config( command=recover_pass)
    submit_btn.pack(pady=(20,10))

def check_rc():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute("SELECT rc FROM allaccounts")
    rcnum = c.fetchall()
    exist = False
    for num in rcnum:
        if num[0] == frc.get():
            exist = True
            break
    
    if exist == False:
        messagebox.showinfo("", "Please check yor code")
    else:
        change_pass()

    conn.commit()
    conn.close()

def recover_pass():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    c.execute("UPDATE allaccounts SET pass = ? WHERE rc = ?", (new_pass_entry.get(), frc.get()))
    messagebox.showinfo("Success", "Your password has been successfully changed.")

    conn.commit()
    conn.close()

def forgot_pass():
    cust_log_scr.destroy()
    global fp,frc
    fp=Tk()
    
    Label(fp, text="Regestaration number", font=("Open Sans", 12, "bold")).pack(padx=(0,130),pady=(10,0))
    frc = Entry(fp, width=30,  border=0,font=("Open Sans", 12))
    frc.pack(padx=(10,0), pady=(10,0))

    nextbtn= Button(fp, text="Next", font=("Open Sans", 12, "bold"), border=0, width=10, bg="#14D8ED", fg="#ffffff", command=check_rc)
    nextbtn.pack(padx=(80,0), pady=(30,0))

    back = Button(fp, text="Go back", font=("Open Sans", 11), border=0, command=cust_login).pack(padx=(70,0), pady=(30,0))

    fp.geometry("400x200+500+200")
    fp.title("Forgot Password")
    fp.mainloop()


def show_passd_ad():
    if c_v2.get()==1:
        ad_password.config(show='')
    else:
        ad_password.config(show="*")

def inc_ad(): #to  go back
    ad_log_scr.destroy()
    wel_screen()

def auth_ad_login():
    if ad_password.get() == "pass" and ad_username.get() == "admin":
        messagebox.showinfo("", "Login Succesful")
    elif ad_password.get() == '' and ad_username.get() == '':
        messagebox.showinfo("", "field must be entered")
    else:
        messagebox.showinfo("", "Invalid admin login")

def inc(): #to go back
    cust_log_scr.destroy()
    wel_screen()

def inc_reg():
    reg_scr.destroy()
    wel_screen()

def show_passd():
    if c_v1.get()==1:
        try:
            password.config(show='')
        except:
            ps_reg.config(show='')
            cps_reg.config(show='')
    else:
        try:
            password.config(show='*')
        except:
            ps_reg.config(show='*')
            cps_reg.config(show='*')


def register():
    global reg_scr
    try:
        cust_log_scr.destroy()
    except:
        pass
    try:
        screen.destroy()
    except:
        pass
    reg_scr = Tk()

    global name,em_reg,rc_reg,ps_reg,cps_reg,c_v1
    rc_number = str(random.randrange(0,999999))
    Label(reg_scr, text="Register", font=("Open Sans", 19, "bold")).place(x=200,y=10)
    Label(reg_scr,text="Name: ",font=("Open Sans", 12)).place(x=30,y=70)
    name = Entry(reg_scr, width=20,  border=0,font=("Open Sans", 12))
    name.place(x=100,y=70)

    Label(reg_scr,text="Email: ",font=("Open Sans", 12)).place(x=30,y=110)
    em_reg = Entry(reg_scr, width=20,  border=0,font=("Open Sans", 12))
    em_reg.place(x=100,y=110)

    Label(reg_scr,text="Registeration Code: ",font=("Open Sans", 12)).place(x=30,y=150)
    def_num = StringVar(value=rc_number)
    rc_reg = Entry(reg_scr,textvariable=def_num, width=20, border=0, font=("Open Sans", 12),state='disable')
    rc_reg.place(x=190,y=150)

    Label(reg_scr,text="Password:",font=("Open Sans", 12),).place(x=30,y=190)
    ps_reg = Entry(reg_scr, width=20,  border=0,font=("Open Sans", 12), show="*")
    ps_reg.place(x=130,y=190)

    Label(reg_scr,text="Confirm Password:",font=("Open Sans", 12),).place(x=30,y=230)
    cps_reg = Entry(reg_scr, width=20,  border=0,font=("Open Sans", 12), show="*")
    cps_reg.place(x=190,y=230)

    c_v1 = IntVar(value=0)
    show_pass = Checkbutton(reg_scr,text="Show Password", variable=c_v1, onvalue=1, offvalue=0,border=0,command=show_passd)
    show_pass.place(x=390,y=230)

    reg_btn = Button(reg_scr, text="Register", font=("Open Sans", 13, "bold"), width=20, border=0, bg="#14D8ED", fg="#fff",command=auth_reg)
    reg_btn.place(x=140,y=300)

    go_back = Button(reg_scr,text="Go back", font=("Open Sans", 12,"bold"), border=0, fg="#14D8ED", command=inc_reg)
    go_back.place(x=140,y=340)
    reg_scr.title("Register")
    reg_scr.geometry("500x400+500+200")
    reg_scr.mainloop()

def auth_login():
    check_username = username.get()
    check_passwd = password.get()
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    acc_login = False
    
    c.execute("SELECT email,pass FROM allaccounts")
    all_acc = c.fetchall()
    for acc in all_acc:
        if acc[0] == check_username and acc[1] == check_passwd:
            acc_login = True
            break

    if check_passwd == '' and check_username == '':
        messagebox.showinfo("", "field must be filled!")
    elif acc_login == True:
        messagebox.showinfo("", "Login Succesful!")
    elif acc_login == False:
        messagebox.showinfo("", "Invalid email or password")


    conn.commit()
    conn.close()


def cust_login():
    try:
        fp.destroy()
    except:
        screen.destroy()
    try:
        reg_scr.destroy()
    except:
        pass
    global cust_log_scr
    cust_log_scr = Tk()

    global username,password,show_pass,c_v1

    Label(cust_log_scr, text="Login",font=("Open Sans", 15,"bold")).pack()

    Label(cust_log_scr, text="Email", font=("Open Sans", 12, "bold")).pack(padx=(0,130),pady=(10,0))
    username = Entry(cust_log_scr, width=30,  border=0,font=("Open Sans", 12))
    username.pack(pady=(5,0))

    Label(cust_log_scr, text="Password", font=("Open Sans", 12, "bold")).pack(padx=(0,130),pady=(20,0))
    password = Entry(cust_log_scr, width=30,  border=0,font=("Open Sans", 12), show="*")
    password.pack(pady=(5,0))

    c_v1 = IntVar(value=0)
    show_pass = Checkbutton(cust_log_scr,text="Show Password", variable=c_v1, onvalue=1, offvalue=0,border=0,command=show_passd)
    show_pass.pack(padx=(0,100))

    forgotpass = Button(cust_log_scr, text="Forgot your password?", border=0, fg="#14D8ED", font=("Open Sans", 10), command=forgot_pass)
    forgotpass.pack()

    register_btn = Button(cust_log_scr, text="Don't have an account? Register",border=0,fg="#14D8ED",font=("Open Sans",10),command=register)
    register_btn.pack()

    login_btn = Button(cust_log_scr,text="Login",font=("Open Sans", 13, "bold"),width=20, border=0,bg="#14D8ED",fg="#fff",command=auth_login)
    login_btn.pack(pady=(20,10))

    back = Button(cust_log_scr, text="Go back", border=0, command=inc).pack(padx=(50,0))

    if count!=0:
        screen()
    
    cust_log_scr.title("login")
    cust_log_scr.geometry("300x350+600+250")
    cust_log_scr.mainloop()


def admin_login():
    global ad_log_scr
    global ad_username, ad_password,show_pass_ad,c_v2
    screen.destroy()

    ad_log_scr = Tk()
    Label(ad_log_scr, text="Login",font=("Open Sans", 15,"bold")).pack()

    Label(ad_log_scr, text="Username", font=("Open Sans", 12, "bold")).pack(padx=(0,130),pady=(10,0))
    ad_username = Entry(ad_log_scr, width=30,  border=0,font=("Open Sans", 12))
    ad_username.pack(pady=(5,0))

    Label(ad_log_scr, text="Password", font=("Open Sans", 12, "bold")).pack(padx=(0,130),pady=(20,0))
    ad_password = Entry(ad_log_scr, width=30,  border=0,font=("Open Sans", 12), show="*")
    ad_password.pack(pady=(5,0))

    c_v2 = IntVar(value=0)
    show_pass_ad = Checkbutton(ad_log_scr,text="Show Password", variable=c_v2, onvalue=1, offvalue=0,border=0,command=show_passd_ad)
    show_pass_ad.pack(padx=(0,100))

    ad_login_btn = Button(ad_log_scr, text="Login", font=("Open Sans",13,"bold"),width=20,border=0,bg="#14D8ED",fg="#fff",command=auth_ad_login)
    ad_login_btn.pack(pady=(20,10))

    back = Button(ad_log_scr, text="Go back", border=0, command=inc_ad).pack(padx=(50,0))

    if count!=0:
        screen()
    
    ad_log_scr.title("login")
    ad_log_scr.geometry("300x350+600+250")
    ad_log_scr.mainloop()
    

def wel_screen():
    global screen
    screen = Tk()
    Label(screen, text="Login",font=("Open Sans", 15,"bold")).grid(padx=(230,0), pady=(20,0))

    admin_btn = Button(screen, text="Admin", font=("Open Sans", 13, "bold"), width=10, border=0, bg="#14D8ED", fg="#fff",command=admin_login)

    customer_btn = Button(screen, text="Student", font=("Open Sans", 13, "bold"), width=10, border=0, bg="#14D8ED",fg="#fff",command=cust_login)

    reg_btn = Button(screen, text="Register", font=("Open Sans", 13, "bold"), width=10, border=0, bg="#14D8ED", fg="#fff",command=register)

    
    admin_btn.grid(padx=(220,0), pady=(40,0))
    customer_btn.grid(padx=(220,0), pady=(40,0))
    reg_btn.grid(padx=(220,0), pady=(40,0))
    
    screen.title("Login")
    screen.geometry("550x400+500+200")
    screen.mainloop()

#LOGIN AND REGISTER ENDS -------------------------------------------------------------------------------------------------------------------

wel_screen()
# conn = sqlite3.connect("accounts.db")
# c = conn.cursor()

# c.execute("""CREATE TABLE allaccounts(
#         name text,
#         email text,
#         pass text,
#         rc text
# )""")

# conn.commit()
# conn.close()
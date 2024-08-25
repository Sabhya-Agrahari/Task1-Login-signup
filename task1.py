import tkinter as tk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random

# Global variables
DATABASE_FILE = "Database.txt"
users = {

}

#Global
n=""

#Generate OTP
def generate_otp(length=6):
    digits = "0123456789"
    return ''.join(random.choice(digits) for i in range(length))

# Send OTP via email
def send_otp_email(email, otp):
    sender_email = "shukla20priyanka@gmail.com"  # Update with your email
    password = "vzsa hidh focw rlph"  # Update with your password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Your OTP"

    body = f"Your OTP is: {otp}"
    msg.attach(MIMEText(body, 'plain'))


    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        messagebox.showinfo("Success", "OTP sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")
       
def login():
    global users  # Ensure we're accessing the global users dictionary
    email = email_entry.get()
    password = password_entry.get()
    
    if email and password:
        load_users()  # Ensure users dictionary is up to date
        print("Loaded users:", users)  # Print loaded users for debugging
        if email in users:
            if users[email]["password"] == password:
                otp = users[email]["otp"]
                hidden_password = '*' * len(password)  
                messagebox.showinfo("Login Details", f"Email: {email}\nPassword: {hidden_password}\nOTP: {otp}")
            else:
                messagebox.showerror("Error", "Invalid password")
        else:
            messagebox.showerror("Error", "User not found. Please register first.")
    else:
        messagebox.showerror("Error", "Please enter email and password")


def signup():
    email = email_entry.get()
    password = password_entry.get()

    if email and password:
        if email in users:
            messagebox.showerror("Error", "Email already exists")
        else:
            users[email] = {"password": password, "otp": ""}
            save_users()  # Save new user to file
            messagebox.showinfo("Success", "Signup Successful")
    else:
        messagebox.showerror("Error", "Please enter email and password")


def request_otp():
    email = email_entry.get()
    if email:
        otp = generate_otp()
        send_otp_email(email, otp)  # Pass both email and otp to send_otp_email
    else:
        messagebox.showerror("Error", "Please enter your email")

def submit():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    address = address_entry.get()

    if name and email and password and address:
        if email in users:
            messagebox.showerror("Error", "Email already exists")
        else:
            try:
                with open(DATABASE_FILE, 'a') as file:
                    file.write(f"Name: {name}, Email: {email}, Password: {password}, Address: {address}\n")
                users[email] = {"password": password, "otp": ""}
                messagebox.showinfo("Success", "Details submitted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit details: {str(e)}")
    else:
        messagebox.showerror("Error", "Please fill in all fields")

#def resendOTP(length=6):
  #  global n  # Access the global variable n
  #  n = generate_otp()
  #  messagebox.showinfo("Success", "OTP Resent: " + n)

def check_database():
    try:
        with open(DATABASE_FILE, 'r') as file:
            data = file.read()
            messagebox.showinfo("Database Content", data)
    except FileNotFoundError:
        messagebox.showerror("Error", "Database file not found")

def load_users():
    global users
    users = {}
    try:
        with open(DATABASE_FILE, 'r') as file:
            for line in file:
                print("Reading line:", line.strip())  # Debug print
                parts = line.strip().split(", ")  # Split by comma and space
                if len(parts) == 3:
                    email = parts[0].split(":")[1].strip()
                    password = parts[1].split(":")[1].strip()
                    address = parts[2].split(":")[1].strip()
                    users[email] = {"password": password, "address": address, "otp": ""}  # Add email, password, and address to users dictionary
                else:
                    print(f"Ignoring line: {line.strip()} (Format doesn't match)")
    except FileNotFoundError:
        pass  # Return an empty dictionary if the file doesn't exist
    return users



def save_users():
    with open(DATABASE_FILE, 'w') as file:
        for email, data in users.items():
            file.write(f"{email}:{data['password']}:{data['otp']}\n")

load_users()

    



root = tk.Tk()
root.title("OTP VERIFIER")
root.geometry('1000x800')
root.resizable(False, False)

canvas = tk.Canvas(root, bg="white", width=600, height=620)
canvas.place(x=100,y=60)
canvas.pack()

heading_text = "REGISTRATION FORM"
canvas.create_text(300, 20, text=heading_text, font=("Arial", 20), fill="Black")

#name box
label = tk.Label(canvas, text="Enter your Full Name:",padx=10, pady=5)
canvas.create_window(100, 120, window=label)
name_entry = tk.Entry(canvas, width=30)
canvas.create_window(350, 120, window=name_entry)


#email box
label = tk.Label(canvas, text="Enter your email address:",padx=10, pady=5)
canvas.create_window(100, 170, window=label)
email_entry = tk.Entry(canvas, width=30)
canvas.create_window(350, 170, window=email_entry)


#send otp 
send_button = tk.Button(canvas, text="Verify Email Address", command=request_otp)
canvas.create_window(520, 220, window=send_button)

#otp box
otp_label = tk.Label(canvas, text="Enter OTP:", padx=10, pady=5)
canvas.create_window(100, 220, window=otp_label)
otp_entry = tk.Entry(canvas, width=30)
canvas.create_window(350, 220, window=otp_entry)

#password box
label = tk.Label(canvas, text="Enter your Password:",padx=10, pady=5)
canvas.create_window(100, 270, window=label)
password_entry = tk.Entry(canvas, width=30,show="*")
canvas.create_window(350, 270, window=password_entry)

#Address box
label = tk.Label(canvas, text="Enter your Address:",padx=10, pady=5)
canvas.create_window(100, 320, window=label)
address_entry = tk.Entry(canvas, width=30)
canvas.create_window(350, 320, window=address_entry)


#login channel
login_button = tk.Button(canvas, text="Login", command=login)
canvas.create_window(450, 70, window=login_button)

#signup channel
signup_button = tk.Button(canvas, text="Signup", command=signup)
canvas.create_window(550, 70, window=signup_button)

submit_button = tk.Button(root, text="SUBMIT", command=submit)
canvas.create_window(300, 370, window=submit_button)




root.mainloop()
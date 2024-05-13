import os
import subprocess
from tkinter import *
from tkinter import Label, Toplevel, Text, Scrollbar, RIGHT, Y, BOTH , messagebox
from tkinter import ttk

"""Creating an interface to allow the user to enter the needed parameters for the cpp code to run"""
"""ALI BDEIR  - Internship @ FEMTO-ST LAB - AS2M DEPARTMENT - Sounkalo DEMBELE  """
"""-----------------------------------------------------------------------------------------------------------"""

"""Note: In the code below there is two paths to be determined , the path for the build file where we can run
the make command in the terminal OR create the build file incase it is not found and the path to the executable file to
run the cpp code. If you are trying to run the code in other machine, you should adapt the paths with your pc ,else the
code will show errors """

directory_path_build = '/home/ali.bdeir/Desktop/Radius_3'
directory_path_cmake = f"{directory_path_build}/build"
directory_path_make = f"{directory_path_build}/build"
executable_path = f"{directory_path_build}/build/main"
text_file_path = "parameters.txt"

# directory_path_build = filedialog.askdirectory(title="Select the path to create the build")
# directory_path_cmake = f"{directory_path_build}/build"
# directory_path_make = f"{directory_path_build}/build"
# executable_path = f"{directory_path_build}/build/main"
# text_file_path = "parameters.txt"


correct_username = "ali.bdeir"
correct_password = "4698"


def authenticate():
    # Function to check if the entered username and password are correct
    entered_username = username_entry.get().lower()
    entered_password = password_entry.get().lower()

    if entered_username == correct_username and entered_password == correct_password:
        # If username and password are correct, open the main interface
        login_window.destroy()  # Close the login window
        win = Tk()
        win.title("Interface for entering the needed parameters")
        win.configure(bg='grey', padx=10, pady=10)
        title_label = Label(
            text="Welcome to the interface\n"
                 "Here you can enter the values of the parameters you defined\n"
                 "Please make sure of the values before proceeding with the steps",
            font=("Helvetica", 16, "bold"),
            justify=CENTER,
            fg='#333',
            bg='grey',
            foreground='white'
        )
        title_label.grid(row=0, column=1, columnspan=8, pady=(20, 10))

        parameters = [
            "ratioo", "numberStep", "X", "filt_Y", "Y", "LOOP", "display",
            "noise", "noiseamplitude", "percentt", "seuil", "iteration", "pas", "seuil_r"
        ]

        parameter_descriptions = {
            "ratioo": "SEM clouds (0.1637)              last clouds:::: 0.04583(u1), 0.05729(u2, u3, n1, n2 and n3), "
                      "1(simuoutils)",
            "numberStep": "maximum value for the loop, to compute the list of the ROI radius.",
            "X": "How much we want to remove data at the beginning",
            "filt_Y": "if we want to filter according to Y",
            "Y": "How much we want to filter according to Y axis",
            "LOOP": "Put 1 if we want to execute a single time, and x value to execute x time, all the algorithms.",
            "display": "put 1 if we want to see the cylinders estimated at each step",
            "noise": "put 1, if we want to add some noise on the point cloud",
            "noiseamplitude": "",
            "percentt": "",
            "seuil": "",
            "iteration": "for the cylinder coefficient",
            "pas": "step between the ROI values.",
            "seuil_r": "threshold of line fitting with LMeDs robest."
        }

        default_values = {
            "ratioo": 1,
            "numberStep": 50,
            "X": 40,
            "filt_Y": "False",
            "Y": 20.0,
            "LOOP": 1,
            "display": 0,
            "noise": 1,
            "noiseamplitude": 0.2,
            "percentt": 100,
            "seuil": 0.1,
            "iteration": 100,
            "pas": 0.1,
            "seuil_r": 0.0001
        }

        entry_values = {}

        for i, parameter in enumerate(parameters):
            label_text = f"Define {parameter}:"
            label = Label(text=label_text, bd=1, font=("Helvetica", 16, "bold"), bg='grey')
            label.grid(row=i + 2, column=1, padx=5, pady=5, sticky="e")

            if parameter == "filt_Y":
                entry = ttk.Combobox(win, values=["True", "False"], width=8, font=("Helvetica", 12, "bold"),
                                     background='grey')
                entry.set(default_values.get(parameter, "False"))
                description_label = Label(win, text="false -  if we want to filter according to Y",
                                          font=("Helvetica", 12, "bold"), fg="blue", bg='grey')
                description_label.grid(row=i + 2, column=4, padx=5, pady=5, sticky="w", columnspan=5)
            elif parameter in parameter_descriptions:
                entry = Spinbox(win, from_=0, to=1000, width=10, font=("Helvetica", 12, "bold"), highlightthickness=0)
                entry.delete(0, END)  # Clear any default value set by Spinbox
                entry.insert(0, default_values.get(parameter, 0))

                description_label = Label(win, text=parameter_descriptions[parameter], font=("Helvetica", 12, "bold"),
                                          fg='blue', bg='grey')
                description_label.grid(row=i + 2, column=4, padx=5, pady=5, sticky="w", columnspan=5)
            else:
                entry = Entry(width=10)
                entry.insert(0, default_values.get(parameter, ""))

            entry.grid(row=i + 2, column=3, padx=5, pady=5, sticky="w")
            entry_values[parameter] = entry

        def get_values_from_file():
            def close_old_window():
                old_window.destroy()

            if 'old_window' in globals():
                close_old_window()

            new_window = Toplevel(win)
            new_window.title("Parameters from File")
            tree = ttk.Treeview(new_window, columns=('Parameter', 'Value'), show='headings')
            tree.heading('Parameter', text='Parameter', anchor='center')
            tree.heading('Value', text='Value', anchor='center')
            bold_font = ("Helvetica", 10, "bold")

            try:
                with open(text_file_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            params, value = line.split()
                            tree.insert('', 'end', values=(params, value))
            except FileNotFoundError:
                print("File 'parameters.txt' not found.")

            tree.tag_configure('bold', font=bold_font)
            tree.tag_bind('bold', '1.0', 'end')
            tree.pack(pady=10)

            global old_window
            old_window = new_window

        # ======================================================================================================================

        def write_parameters_to_file():
            confirmation = messagebox.askyesno("Confirmation", "Do you want to save parameters to 'parameters.txt'?")

            parameters_dict = {}
            if confirmation:
                messagebox.showinfo(message="Data is saved successfully")
                print("Parameters written to 'parameters.txt'.")
                for param, entryy in entry_values.items():
                    if param == "filt_Y":
                        # Convert to boolean
                        parameters_dict[param] = str(int(entryy.get() == "True"))
                    else:
                        try:
                            # Try converting to float (for numbers)
                            parameters_dict[param] = str(float(entryy.get()))

                        except ValueError:
                            # If conversion fails, keep the original value (could be a string)
                            parameters_dict[param] = entryy.get()

            else:
                print('Parameters not saved !')
                messagebox.showinfo(message="Parameters not saved !")

            with open("parameters.txt", "w") as txt_file:
                for param, value in parameters_dict.items():
                    txt_file.write(f"{param} {value}\n")

        result_text = StringVar()

        result_window = None

        def show_result_window(output_texts):
            # Close the existing result window, if it exists
            global result_window
            if result_window and result_window.winfo_exists():
                result_window.destroy()

            # Create a new result window
            result_window = Toplevel(win)
            result_window.title("C++ Build and Run Result")

            # Create a Text widget for displaying output
            result_text = Text(result_window, wrap="word", font=("Helvetica", 12, "bold"), padx=10, pady=10,
                               background="grey", foreground="black", width=80, height=20)
            result_text.pack(expand=True, fill=BOTH)

            # Create a Scrollbar and attach it to the Text widget
            scrollbar = Scrollbar(result_window, command=result_text.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            result_text.configure(yscrollcommand=scrollbar.set)

            # Insert the output text into the Text widget
            result_text.insert("1.0", output_texts)

        def reset_to_defaults():
            y = messagebox.askyesno(message="Are you sure you want to set the values to default?", title="Warning!")
            if y:
                for param, entry_widget in entry_values.items():
                    if param == "filt_Y":
                        entry_widget.set(default_values.get(param, "False"))
                    elif param in parameter_descriptions:
                        entry_widget.delete(0, END)
                        entry_widget.insert(0, default_values.get(param, 0))
                    else:
                        entry_widget.delete(0, END)
                        entry_widget.insert(0, default_values.get(param, ""))

            messagebox.showinfo(message="Parameters are set to default.\n\n"
                                        "Don't forget to save before continuing!",
                                title="Info")

        # ======================================================================================================================

        def run_build_command_in_directory():
            confirmations = messagebox.askyesno(message="Are you sure you want to compile this code?", title="Warning!")
            if confirmations:
                try:
                    original_directory = os.getcwd()
                    os.chdir(directory_path_build)
                except FileNotFoundError:
                    print(f"Error: The directory '{directory_path_build}' does not exist.")
                    return
                except Exception as e:
                    print(f"Error: {e}")
                    return

                # Run the make command
                try:
                    os.makedirs('build', exist_ok=True)
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    # Change back to the original directory
                    os.chdir(original_directory)
                    run_cmake_command()
            else:
                show_popup(inp="Cancelled")

        def run_cmake_command():
            try:
                original_directory = os.getcwd()
                os.chdir(directory_path_cmake)
            except FileNotFoundError:
                print(f"Error: The directory '{directory_path_cmake}' does not exist.")
                return
            except Exception as e:
                print(f"Error: {e}")
                return

            # Run the cmake command and capture output in real-time
            output_text = ""
            try:
                cmake_process = subprocess.Popen(['cmake', '..'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                 text=True, bufsize=1, universal_newlines=True)

                # Display cmake output live and capture it in the variable
                for line in iter(cmake_process.stdout.readline, ''):
                    output_text += line
                    print(line, end='')

                # Wait for the cmake process to finish
                cmake_process.wait()

            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                output_text += f"Error: {e}\n"
            except Exception as e:
                print(f"Unexpected error: {e}")
                output_text += f"Unexpected error: {e}\n"
            finally:
                # Change back to the original directory
                os.chdir(original_directory)
                show_popup(output_text)

        def run_make_command_in_directory():
            messagebox.showinfo(message="Make sure to compile before!", title="Warning!")
            try:
                os.chdir(directory_path_make)
            except FileNotFoundError:
                print(f"Error: The directory '{directory_path_make}' does not exist.")
                messagebox.showerror(message=f"Error: The directory '{directory_path_make}' does not exist.\n\n"
                                             f"Try Build and Compile before!")
                return
            except Exception as e:
                print(f"Error: {e}")
                show_popup(e)
                return

            # Run the make command
            try:
                result = subprocess.run(['make'], capture_output=True, text=True, check=True)
                output_text = result.stdout
                error_text = result.stderr  # If you also want to capture error output

                print("Make command output:")
                show_popup(output_text)

                if error_text:
                    print("Make command error output:")
                    print(error_text)
                    show_popup(output_text)

            except subprocess.CalledProcessError as e:
                print("Error executing 'make' command. Return code:", e.returncode)
                print("Error output:")
                print(e.stderr)
                show_popup(e.stderr)
            finally:
                # Change back to the original directory
                os.chdir(os.path.dirname(os.path.abspath(__file__)))

        def run_executable():
            output_text = ""
            try:
                # Run the executable and capture output
                process = subprocess.Popen([executable_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Wait for the process to finish and get the output
                stdout, stderr = process.communicate()

                # Store the output in the output_text string
                output_text += f"Standard Output:\n{stdout}\n\n"
            except FileNotFoundError:
                print(f"Error: Executable '{executable_path}' not found.")
            except subprocess.CalledProcessError as e:
                print(f"Error: Execution of '{executable_path}' failed with return code {e.returncode}.")
            except Exception as e:
                print(f"Unexpected error: {e}")

            show_result_window(output_texts=output_text)

        def show_popup(inp):
            messagebox.showinfo(message=inp, title="DONE")

        # save parameters button
        button = Button(text="Save the Parameters", command=write_parameters_to_file, bg="red", foreground="white",
                        highlightthickness=0, font=("Helvetica", 10, "bold"))
        button.grid(row=len(parameters) + 2, column=1, columnspan=3, pady=10)

        # display button
        display_button = Button(text="Display current Values", command=get_values_from_file, bg="red",
                                foreground="white",
                                highlightthickness=0, font=("Helvetica", 10, "bold"))
        display_button.grid(row=len(parameters) + 2, column=3, columnspan=5, pady=10)

        # reset to default button
        reset_default_button = Button(text="Default Values", bg="red", foreground="white", command=reset_to_defaults,
                                      highlightthickness=0, font=("Helvetica", 10, "bold"))
        reset_default_button.grid(row=len(parameters) + 2, column=7, columnspan=8, pady=10)

        build_button = Button(text="Build and Compile", bg="black", foreground="white",
                              command=run_build_command_in_directory,
                              highlightthickness=0, font=("Helvetica", 10, "bold"))
        build_button.grid(row=len(parameters) + 3, column=1, columnspan=3, pady=10)

        make_button = Button(text="make", bg="black", foreground="white", command=run_make_command_in_directory,
                             highlightthickness=0, font=("Helvetica", 10, "bold"), width=20)
        make_button.grid(row=len(parameters) + 3, column=3, columnspan=5, pady=10)

        run_button = Button(text="Run C++ code", bg="black", foreground="white", command=run_executable,
                            highlightthickness=0, font=("Helvetica", 10, "bold"))
        run_button.grid(row=len(parameters) + 3, column=7, columnspan=8, pady=10)

        win.mainloop()

    else:
        # If username or password is incorrect, show an error message
        messagebox.showerror("Authentication Failed", "Incorrect username or password")


def open_registration_window():
    registration_window = Toplevel(login_window)
    registration_window.title("Register")
    registration_window.geometry("300x200")

    # Add registration window components here
    # Example: registration_label = Label(registration_window, text="Registration Window")
    # Example: registration_label.pack()

def open_forgot_password_window():
    forgot_password_window = Toplevel(login_window)
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("300x150")

    # Add forgot password window components here
    # Example: forgot_password_label = Label(forgot_password_window, text="Forgot Password Window")
    # Example: forgot_password_label.pack()

login_window = Tk()
login_window.title("Login")
login_window.configure(bg='grey', padx=10, pady=10)

# Add a frame with a border
frame = Frame(login_window, bg='white', relief='raised', borderwidth=2)
frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Add username and password labels and entry widgets
username_label = Label(frame, text="Username:", font=("Helvetica", 12, "bold"), bg='white')
username_label.grid(row=0, column=0, pady=5, sticky="e")

password_label = Label(frame, text="Password:", font=("Helvetica", 12, "bold"), bg='white')
password_label.grid(row=1, column=0, pady=5, sticky="e")

username_entry = Entry(frame, width=20)
username_entry.grid(row=0, column=1, pady=5, sticky="w")

password_entry = Entry(frame, width=20, show="*")  # Use show="*" to display '*' for password
password_entry.grid(row=1, column=1, pady=5, sticky="w")

# Add a styled login button
login_button = Button(login_window, text="Login", command=authenticate, bg="#4CAF50", fg="white",
                      highlightthickness=0, font=("Helvetica", 12, "bold"), relief='flat')
login_button.grid(row=1, column=0, columnspan=2, pady=10)

# Add a "Forgot Password" link
forgot_password_link = Label(login_window, text="Forgot Password?", font=("Helvetica", 10), bg='grey', fg='blue', cursor='hand2')
forgot_password_link.grid(row=2, column=0, columnspan=2, pady=5)
forgot_password_link.bind("<Button-1>", lambda e: open_forgot_password_window())

# Add a registration button
register_button = Button(login_window, text="Register", command=open_registration_window, bg="orange", fg="white",
                         highlightthickness=0, font=("Helvetica", 12, "bold"), relief='flat')
register_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start the Tkinter main loop for the login window
login_window.mainloop()



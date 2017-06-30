from Tkinter import *
import tkFileDialog as fd
import ttk
import os
import time
from build_matrix import *
from net_comp.network_comparison import *
from sys import platform
import subprocess as sub

SCALE_X = 0.3
SCALE_Y = 0.7

try: 
    import ctypes
    
    user32 = ctypes.windll.user32

    WIDTH, HEIGHT = int(SCALE_X*user32.GetSystemMetrics(0)), int(SCALE_Y*user32.GetSystemMetrics(1))
except:
    WIDTH, HEIGHT = (300, 650)
    
PADX = 5
PADY = 5

C0 = '#FFFFFF'
C1 = '#76B8B8'
C2 = '#459393'
C3 = '#2B7E7E'
C4 = '#176C6C'
C5 = '#085656'
CR = 'red'

XSMALL_FONT = ('Segoe UI Regular', 8)
SMALL_FONT = ('Segoe UI Regular', 10)
LABEL_FONT = ('Segoe UI Semibold', 14)
MEDIUM_FONT = ('Segoe UI Regular', 22)
LARGE_FONT = ('Segoe UI Regular', 30)

class NetworkUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        self.title("Network Utility")
        self.geometry('{0}x{1}'.format(WIDTH, HEIGHT))
        self.visualize_choice = BooleanVar()
        
        ttk.Style().configure("TButton", padding=4, font=SMALL_FONT, foreground=C5)
        ttk.Style().configure("TRadiobutton", padding=4, font=SMALL_FONT, foreground=C1, background=C5)
        ttk.Style().configure("TSeparator", padding=4, background=C5)
        
        ttk.Style().configure("Exit.TButton", padding=4, font=SMALL_FONT, foreground=CR)
        ttk.Style().configure("Run.TButton", padding=4, font=SMALL_FONT, foreground=C5)
        
        ttk.Style().configure("TNotebook", padding=6, font=SMALL_FONT, background=C1)
        
        self.open_intro_menu()
        
    def open_intro_menu(self):
        
        try:
            self.network_builder_tab.destroy()            
        except:
            print "Network Builder Tab not opened yet!"
            
        try:
            self.network_comparison_tab.destroy()
        except:
            print "Network Comparison Tab not opened yet!"
            
        self.intro_menu = Frame(self, bg=C5)
        
        self.build_network_button = ttk.Button(self.intro_menu, text="Create Network", width=20, command=self.open_network_builder)
        self.build_network_button.grid(row=0, column=0, padx=PADX, pady=PADY)
        
        self.compare_network_button = ttk.Button(self.intro_menu, text="Compare Networks", width=20, command=self.comparison_size)
        self.compare_network_button.grid(row=1, column=0, padx=PADX, pady=PADY)
        
        exit_button = ttk.Button(self.intro_menu, text="Exit", width=20, command=self.quit, style="Exit.TButton")
        exit_button.grid(row=2, column=0, padx=PADX, pady=PADY)
        
        self.intro_menu.place(relx=0.5, rely=0.5, anchor="center")
        
    def open_single_network_comparison(self):
        self.intro_menu.destroy()
        self.comparison_size_tab.destroy()
        
        self.network_comparison_tab = Frame(self, bg=C5)
        
        muni_name_label = Label(self.network_comparison_tab, text="Municipality Name", font=LABEL_FONT, bg=C5, fg=C1)
        muni_name_label.grid(row=0, column=0, padx=PADX, pady=PADY)
        
        self.muni_name = Entry(self.network_comparison_tab, font=SMALL_FONT, width=20, relief=FLAT, fg=C4)
        self.muni_name.grid(row=1, column=0, padx=PADX, pady=PADY)
        
        networkA_label = Label(self.network_comparison_tab, text="Choose Network A", font=LABEL_FONT, bg=C5, fg=C1)
        networkA_label.grid(row=2, column=0, padx=PADX, pady=PADY)
        
        self.choose_networkA_button = ttk.Button(self.network_comparison_tab, text="Browse", width=20, command=self.choose_networkA)
        self.choose_networkA_button.grid(row=3, column=0, padx=PADX, pady=PADY)
        
        self.chosen_networkA_label = Label(self.network_comparison_tab, text="[No File Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.chosen_networkA_label.grid(row=4, column=0, padx=PADX, pady=PADY)
        
        networkB_label = Label(self.network_comparison_tab, text="Choose Network B", font=LABEL_FONT, bg=C5, fg=C1)
        networkB_label.grid(row=5, column=0, padx=PADX, pady=PADY)
        
        self.choose_networkB_button = ttk.Button(self.network_comparison_tab, text="Browse", width=20, command=self.choose_networkB)
        self.choose_networkB_button.grid(row=6, column=0, padx=PADX, pady=PADY)
        
        self.chosen_networkB_label = Label(self.network_comparison_tab, text="[No File Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.chosen_networkB_label.grid(row=7, column=0, padx=PADX, pady=PADY)
        
        choose_comp_output_folder = Label(self.network_comparison_tab, text="Choose Output Folder", font=LABEL_FONT, bg=C5, fg=C1)
        choose_comp_output_folder.grid(row=8, column=0, padx=PADX, pady=PADY)
        
        self.choose_compare_output_folder_button = ttk.Button(self.network_comparison_tab, text="Browse", width=20, command=self.choose_compare_network_output_folder)
        self.choose_compare_output_folder_button.grid(row=9, column=0, padx=PADX, pady=PADY)
        
        self.chosen_compare_output_folder_label = Label(self.network_comparison_tab, text="[No File Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.chosen_compare_output_folder_label.grid(row=10, column=0, padx=PADX, pady=PADY)
        
        ttk.Separator(self.network_comparison_tab).grid(row=11, column=0, padx=PADX, pady=PADY, sticky="EW")
        
        self.run_compare_network_button = ttk.Button(self.network_comparison_tab, text="Compare", width=20, command=self.compare_networks_single)
        self.run_compare_network_button.grid(row=12, column=0, padx=PADX, pady=PADY)
        
        self.compare_progress_status = Label(self.network_comparison_tab, text="", font=LABEL_FONT, bg=C5, fg=CR)
        self.compare_progress_status.grid(row=13, column=0, padx=PADX, pady=PADY)
        
        self.open_comparison_output_button = ttk.Button(self.network_comparison_tab, text="Open Output", width=20, command=self.open_comparison_output)
        self.open_comparison_output_button.grid(row=14, column=0, padx=PADX, pady=PADY)
        
        self.home_button = ttk.Button(self.network_comparison_tab, text="Home", width=20, command=self.open_intro_menu)
        self.home_button.grid(row=15, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        exit_button = ttk.Button(self.network_comparison_tab, text="Exit", width=20, command=self.quit, style="Exit.TButton")
        exit_button.grid(row=16, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        
        self.network_comparison_tab.place(relx=0.5, rely=0.5, anchor="center")
    
    def open_multiple_network_comparison(self):
        self.intro_menu.destroy()
        self.comparison_size_tab.destroy()
        
        self.network_comparison_tab = Frame(self, bg=C5)
        
        networksA_label = Label(self.network_comparison_tab, text="Choose Networks A Folder", font=LABEL_FONT, bg=C5, fg=C1)
        networksA_label.grid(row=1, column=0, padx=PADX, pady=PADY)
        
        self.choose_networksA_button = ttk.Button(self.network_comparison_tab, text="Browse", width=20, command=self.choose_networksA)
        self.choose_networksA_button.grid(row=2, column=0, padx=PADX, pady=PADY)
        
        self.chosen_networksA_label = Label(self.network_comparison_tab, text="[No Folder Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.chosen_networksA_label.grid(row=3, column=0, padx=PADX, pady=PADY)
        
        networksB_label = Label(self.network_comparison_tab, text="Choose Networks B Folder", font=LABEL_FONT, bg=C5, fg=C1)
        networksB_label.grid(row=4, column=0, padx=PADX, pady=PADY)
        
        self.choose_networksB_button = ttk.Button(self.network_comparison_tab, text="Browse", width=20, command=self.choose_networksB)
        self.choose_networksB_button.grid(row=5, column=0, padx=PADX, pady=PADY)
        
        self.chosen_networksB_label = Label(self.network_comparison_tab, text="[No Folder Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.chosen_networksB_label.grid(row=6, column=0, padx=PADX, pady=PADY)
        
        choose_comp_output_folder = Label(self.network_comparison_tab, text="Choose Output Folder", font=LABEL_FONT, bg=C5, fg=C1)
        choose_comp_output_folder.grid(row=7, column=0, padx=PADX, pady=PADY)
        
        self.choose_compare_output_folder_button = ttk.Button(self.network_comparison_tab, text="Browse", width=20, command=self.choose_compare_network_output_folder)
        self.choose_compare_output_folder_button.grid(row=8, column=0, padx=PADX, pady=PADY)
        
        self.chosen_compare_output_folder_label = Label(self.network_comparison_tab, text="[No Folder Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.chosen_compare_output_folder_label.grid(row=9, column=0, padx=PADX, pady=PADY)
        
        ttk.Separator(self.network_comparison_tab).grid(row=10, column=0, padx=PADX, pady=PADY, sticky="EW")
        
        self.run_compare_network_button = ttk.Button(self.network_comparison_tab, text="Compare", width=20, command=self.compare_networks_multiple)
        self.run_compare_network_button.grid(row=11, column=0, padx=PADX, pady=PADY)
        
        self.compare_progress_status = Label(self.network_comparison_tab, text="", font=LABEL_FONT, bg=C5, fg=CR)
        self.compare_progress_status.grid(row=12, column=0, padx=PADX, pady=PADY)
        
        self.open_comparison_output_button = ttk.Button(self.network_comparison_tab, text="Open Output", width=20, command=self.open_comparison_output)
        self.open_comparison_output_button.grid(row=13, column=0, padx=PADX, pady=PADY)
        
        self.home_button = ttk.Button(self.network_comparison_tab, text="Home", width=20, command=self.open_intro_menu)
        self.home_button.grid(row=14, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        exit_button = ttk.Button(self.network_comparison_tab, text="Exit", width=20, command=self.quit, style="Exit.TButton")
        exit_button.grid(row=16, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        
        self.network_comparison_tab.place(relx=0.5, rely=0.5, anchor="center")
    
    def open_comparison_output(self, ):
        if platform == 'darwin':
            sub.Popen(['open', self.selected_compare_output_folder])
        elif platform == 'linux' or platform == 'linux2':
            sub.Popen(['nautilus', self.selected_compare_output_folder])
        elif platform == 'win32':
            sub.Popen(['explorer', self.selected_compare_output_folder])
    
    def choose_compare_network_output_folder(self):
        try:
            dir_history = open('recent_directory.txt', 'r').read()
            
            self.selected_compare_output_folder = fd.askdirectory(initialdir=dir_history.strip(), title="Choose Output Folder")
            
            if len(self.selected_compare_output_folder) > 0:
                
                self.chosen_compare_output_folder_label.configure(text=self.selected_compare_output_folder.split("/")[-1], fg="orange")
                
                with open('recent_directory.txt', 'w') as f:
                    f.write(self.selected_compare_output_folder)
                
            else:
                print "\n\nNo Folder selected\n\n"
                self.chosen_compare_output_folder_label.configure(text="[No Folder Selected]", fg="red")
                
        except Exception, e:
            print e
    
    def compare_networks_single(self):
        self.compare_progress_status.configure(text="Working...", fg=CR)
        self.update()
        
        comparison = NetworkComparisonSingle(self.muni_name.get(), self.networkA_file, self.networkB_file, wd=self.selected_compare_output_folder)
        comparison.get_comparison_summary()
        
        self.update()
        self.compare_progress_status.configure(text="Finished", fg="green")
        
    def compare_networks_multiple(self):
        self.compare_progress_status.configure(text="Working...", fg=CR)
        self.update()
        
        wdA = self.networkA_folder
        wdB = self.networkB_folder
        
        networks_A = [f for f in os.listdir(wdA) if f.lower().endswith('.csv')]
        networks_B = [f for f in os.listdir(wdB) if f.lower().endswith('.csv')]
        
        matches = list(set(networks_A).intersection(networks_B))
        
        networks_A = [wdA + '/' + f for f in matches]
        networks_B = [wdB + '/' + f for f in matches]
        
        output_path = self.selected_compare_output_folder + '/Comparison Summary'
        
        if not os.path.exists(output_path):
            os.mkdir(output_path)
            print "Created: {0}".format(output_path)
            
        for n in range(len(matches)):
            muni_name = ' '.join(matches[n].replace('_adjacency_matrix.csv', '').split('_')).title()
            
            nA = networks_A[n]
            nB = networks_B[n]
            
            
            comparison = NetworkComparisonSingle(muni_name, nA, nB, wd=output_path)
            comparison.get_comparison_summary()
            
        self.update()
        self.compare_progress_status.configure(text="Finished", fg="green")
        
    def choose_networkA(self):        
        dir_history = open('recent_directory.txt', 'r').read()
        
        self.networkA_file = fd.askopenfilename(initialdir=dir_history.strip(), title="Choose Network A")
        
        if len(self.networkA_file) > 0:
            self.chosen_networkA_label.configure(text=self.networkA_file.split('/')[-1], fg="orange")
            
        else:
            print "No file selected!"
            self.chosen_networkA_label.configure(text="[No File Selected]", fg=CR)
    
    def choose_networksA(self):        
        dir_history = open('recent_directory.txt', 'r').read()
        
        self.networkA_folder = fd.askdirectory(initialdir=dir_history.strip(), title="Choose Networks A Folder")
        
        if len(self.networkA_folder) > 0:
            self.chosen_networksA_label.configure(text=self.networkA_folder.split('/')[-1], fg="orange")
            
        else:
            print "No folder selected!"
            self.chosen_networksA_label.configure(text="[No Folder Selected]", fg=CR)
    
    
    def choose_networkB(self):
        
        self.networkB_file = fd.askopenfilename(title="Choose Network B")
        
        if len(self.networkB_file) > 0:
            self.chosen_networkB_label.configure(text=self.networkB_file.split('/')[-1], fg="orange")
        else:
            print "No file selected!"
            self.chosen_networkB_label.configure(text="[No File Selected]", fg=CR)
    
    def choose_networksB(self):
        dir_history = open('recent_directory.txt', 'r').read()
        
        self.networkB_folder = fd.askdirectory(initialdir=dir_history.strip(), title="Choose Networks B Folder")
        
        if len(self.networkB_folder) > 0:
            self.chosen_networksB_label.configure(text=self.networkB_folder.split('/')[-1], fg="orange")
        else:
            print "No file selected!"
            self.chosen_networksB_label.configure(text="[No Folder Selected]", fg=CR)
        
    def comparison_size(self):
        self.intro_menu.destroy()
        self.comparison_size_tab = Frame(self, bg=C5)
        
        comparison_size = Label(self.comparison_size_tab, text="How many comparisons?", font=LABEL_FONT, bg=C5, fg=C1)
        comparison_size.grid(row=0, column=0, padx=PADX, pady=PADY)
        
        self.single_button = ttk.Button(self.comparison_size_tab, text="Single", width=20, command=self.open_single_network_comparison)
        self.single_button.grid(row=1, column=0, padx=PADX, pady=PADY)
        
        self.multiple_button = ttk.Button(self.comparison_size_tab, text="Multiple", width=20, command=self.open_multiple_network_comparison)
        self.multiple_button.grid(row=2, column=0, padx=PADX, pady=PADY)
        
        exit_button = ttk.Button(self.comparison_size_tab, text="Exit", width=20, command=self.quit, style="Exit.TButton")
        exit_button.grid(row=16, column=0, padx=PADX, pady=PADY)
        
        
        self.comparison_size_tab.place(relx=0.5, rely=0.5, anchor="center")
    
    def open_network_builder(self):
        self.intro_menu.destroy()
        self.network_builder_tab = Frame(self, bg=C5)
        
        self.selected_att_folder = None
        
        choose_event_files_label = Label(self.network_builder_tab, text="Choose Event Files", font=LABEL_FONT, bg=C5, fg=C1)
        choose_event_files_label.grid(row=0, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.choose_event_files_button = ttk.Button(self.network_builder_tab, text="Browse", width=20, command=self.choose_event_files)
        self.choose_event_files_button.grid(row=1, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.selected_event_files_label = Label(self.network_builder_tab, text="[No Files Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.selected_event_files_label.grid(row=2, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        choose_output_folder_label = Label(self.network_builder_tab, text="Choose Output Folder", font=LABEL_FONT, bg=C5, fg=C1)
        choose_output_folder_label.grid(row=3, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.choose_output_folder_button = ttk.Button(self.network_builder_tab, text="Browse", width=20, command=self.choose_output_folder)
        self.choose_output_folder_button.grid(row=4, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.selected_output_folder_label = Label(self.network_builder_tab, text="[No Folder Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.selected_output_folder_label.grid(row=5, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        choose_att_files_label = Label(self.network_builder_tab, text="Choose Attributes Folder*", font=LABEL_FONT, bg=C5, fg=C1)
        choose_att_files_label.grid(row=6, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.choose_att_folder_button = ttk.Button(self.network_builder_tab, text="Browse", width=20, command=self.choose_att_folder)
        self.choose_att_folder_button.grid(row=7, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.selected_att_files_label = Label(self.network_builder_tab, text="[No Folder Selected]", fg=CR, bg=C5, font=SMALL_FONT)
        self.selected_att_files_label.grid(row=8, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        visualize_label = Label(self.network_builder_tab, text="Visualize Results", font=LABEL_FONT, bg=C5, fg=C1)
        visualize_label.grid(row=9, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.no_button = ttk.Radiobutton(self.network_builder_tab, text="No", variable=self.visualize_choice, value=False, command=self.show_choice)
        self.no_button.grid(row=10, column=1, padx=PADX, pady=PADY)
        
        self.yes_button = ttk.Radiobutton(self.network_builder_tab, text="Yes", variable=self.visualize_choice, value=True, command=self.show_choice)
        self.yes_button.grid(row=10, column=2, padx=PADX, pady=PADY)
        
        optional_label = Label(self.network_builder_tab, text="*Optional", font=XSMALL_FONT, bg=C5, fg=C1)
        optional_label.grid(row=11, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        ttk.Separator(self.network_builder_tab).grid(row=12, column=1, columnspan=2, padx=PADX, pady=PADY*2, sticky="EW")
        
        self.run_button = ttk.Button(self.network_builder_tab, text="Run", width=20, style="Run.TButton", command=self.run_build_matrix)
        self.run_button.grid(row=13, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.progress_status = Label(self.network_builder_tab, text="", font=LABEL_FONT, bg=C5, fg=CR)
        self.progress_status.grid(row=14, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.open_nb_output_button = ttk.Button(self.network_builder_tab, text="Open Output", width=20, command=self.open_net_build_output)
        self.open_nb_output_button.grid(row=15, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.home_button = ttk.Button(self.network_builder_tab, text="Home", width=20, command=self.open_intro_menu)
        self.home_button.grid(row=16, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        exit_button = ttk.Button(self.network_builder_tab, text="Exit", width=20, command=self.quit, style="Exit.TButton")
        exit_button.grid(row=17, column=0, columnspan=4, padx=PADX, pady=PADY)
        
        self.network_builder_tab.place(relx=0.5, rely=0.5, anchor="center")
    
    
    def choose_event_files(self):
        try:
            dir_history = open('recent_directory.txt', 'r').read()
            
            self.selected_event_files = fd.askopenfilenames(initialdir=dir_history.strip(), title="Choose Event Files")
            
            if len(self.selected_event_files) > 0:
                
                self.working_directory = "/".join(self.selected_event_files[0].split("/")[:-1]) + "/"
                
                multiple = 's' if len(self.selected_event_files) > 1 else ''
                
                self.selected_event_files_label.configure(text="{0} file{1} selected".format(len(self.selected_event_files), multiple), fg="orange")
                
                with open('recent_directory.txt', 'w') as f:
                    f.write(self.working_directory)
                
            else:
                print "\n\nNo files selected\n\n"
                self.selected_event_files_label.configure(text="[No Files Selected]", fg="red")
                
        except Exception, e:
            print e
    
    def choose_att_folder(self):
        try:
            dir_history = open('recent_directory.txt', 'r').read()
            
            self.selected_att_folder = fd.askdirectory(initialdir=dir_history.strip(), title="Choose Attributes Folder")
            
            if len(self.selected_att_folder) > 0:
                
                self.selected_att_files_label.configure(text=self.selected_att_folder.split('/')[-1], fg="orange")
                
            else:
                print "\n\nNo folder selected\n\n"
                self.selected_att_files_label.configure(text="[No Folder Selected]", fg="red")
                self.selected_att_folder = None
                
        except Exception, e:
            print e
            
    def choose_output_folder(self):
        try:
            dir_history = open('recent_directory.txt', 'r').read()
            
            self.selected_output_folder = fd.askdirectory(initialdir=dir_history.strip(), title="Choose Output Folder")
            
            if len(self.selected_output_folder) > 0:
                
                self.selected_output_folder_label.configure(text=self.selected_output_folder.split("/")[-1], fg="orange")
                
                with open('recent_directory.txt', 'w') as f:
                    f.write(self.selected_output_folder)
                
            else:
                print "\n\nNo Folder selected\n\n"
                self.selected_output_folder_label.configure(text="[No Folder Selected]", fg="red")
                
        except Exception, e:
            print e
            
    def run_build_matrix(self):
        try:
            self.progress_status.configure(text="Working...", fg=CR)
            self.update()
            
            if self.selected_att_folder != None:
                att_files = [f for f in os.listdir(self.selected_att_folder) if f.endswith('.csv') and "attributes" in f.lower()]
            
            for event_file in self.selected_event_files:
                print event_file
                
                if self.selected_att_folder != None:
                    corresponding_att_file = "{0} attributes.csv".format(event_file.split('/')[-1].split('Relationships')[0].strip().lower())
                    
                    current_attribute_file = [f for f in att_files if corresponding_att_file in f.lower()]
                    
                    if len(current_attribute_file) > 0:
                        current_attribute_file = current_attribute_file[0]
                    else:
                        current_attribute_file = None
                    
                else:
                    current_attribute_file = None
                    
                adj_mat = AdjacencyMatrix(event_file, self.selected_output_folder, attributes=current_attribute_file, visualize=self.visualize_choice.get())
                adj_mat.run()
            
            self.update()
            self.progress_status.configure(text="Finished", fg='green')
                
        except Exception, e:
            print e
            
    def open_net_build_output(self):
        try:
            if platform == 'darwin':
                sub.Popen(['open', self.selected_output_folder])
            elif platform == 'win32':
                sub.Popen(['explorer', self.selected_output_folder])
            elif platform == 'linux' or platform == 'linux2':
                sub.Popen(['nautilus', self.selected_output_folder])
            
        except Exception, e:
            print e
            
    def show_choice(self):
        print self.visualize_choice.get()
        
app = NetworkUI()
app.configure(background=C4)
app.mainloop()
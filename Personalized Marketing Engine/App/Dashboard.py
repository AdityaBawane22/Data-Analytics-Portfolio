import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import os

from Data_Aggregation import get_cluster_summary
from Visuals_Combiner import VisualsViewerWindow
from Phone_Mockup import PhoneMockup  
from Ollama_prompt_file import generate_ollama_message
from Monthly_Events_List import EVENTS_LIST  

ADMIN_NAME = "Aditya"

OFFER_PROPOSALS = {
    0: {'segment': "Steady (Consistent Performers)",
        'goal': "Reward & Retain - Make them feel exclusive and valued.",
        'offers': ['VIP Access', 'Double Loyalty Points', 'Discount', 'Private Sale Invite']},
    1: {'segment': "Emerging (Growing Engagement)",
        'goal': "Engage & Inspire - Encourage more frequent purchases.",
        'offers': ['Free Styling', 'Gift Wrapping', 'Free Shipping', 'Early Lookbook']},
    2: {'segment': "Mature (Maximize Value)",
        'goal': "Increase Average Order Value - Boost transaction size.",
        'offers': ['Bundle Offer', 'Free Accessory', 'Cashback', 'Product Samples']},
    3: {'segment': "Leading (At-Risk Recovery)",
        'goal': "Re-activate & Repair - Bring customers back.",
        'offers': ['Discount', 'Priority Support', 'Reactivation Voucher', 'Thank You Gift']},
    -1: {'segment': "Initial (New/Monitor)",
        'goal': "Monitor & Standardize - Low-touch, cost-effective.",
        'offers': ['Seasonal Discount', 'Flash Sale', 'Referral Rewards', 'Birthday Discount']}
}

def get_event_for_date(date):
    """Return the event name for a given date, or None if no event."""
    month = date.month
    day = date.day
    for m, d, event_name in EVENTS_LIST:
        if m == month and d == day:
            return event_name
    return None

class MarketingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personalized Marketing Engine")
        self.configure(bg="#FFA500")

        
        self.state("zoomed")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background="#FF5F1F")
        style.configure('TLabel', background="#FF5F1F", foreground='#000000')
        style.configure('TButton', font=('Arial', 10, 'bold'), foreground='black', background='#CCD1D1')
        style.configure('Header.TLabel', font=('Arial', 24, 'bold'), foreground='#F1C40F')
        style.configure('Accent.TButton', background='#008000', foreground='white', font=('Arial', 12, 'bold'))
        style.configure('Card.TFrame', background='#001F3F', relief='raised')
        style.configure('CardHeader.TLabel', background='#001F3F', foreground='#F1C40F', font=('Arial', 14, 'bold'))
        style.configure('Text.TLabel', background='#001F3F', foreground='white', font=('Arial', 11))

        self.selected_date = datetime.datetime.now()
        self.phone_mockup_window = None  

        
        json_path = r'C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\P1\cluster_data.json'
        csv_path = r'C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\Raw_data\Dataset.csv'

        self.cluster_summary = get_cluster_summary(json_path, csv_path)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, ClusterDetailPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name, cluster_id=None):
        frame = self.frames[page_name]
        if page_name == "ClusterDetailPage" and cluster_id is not None:
            frame.update_display(cluster_id)
        frame.tkraise()

    def get_summary_for_cluster(self, cluster_id):
        data = self.cluster_summary.get(int(cluster_id), {'num_customers': 0, 'total_revenue_inr': 0})
        return {'customers': data['num_customers'], 'revenue': data['total_revenue_inr']}


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = ttk.Frame(self, padding="20 10 20 10")
        header_frame.pack(fill='x')

        self.greeting_label = ttk.Label(header_frame, text="", style='Header.TLabel')
        self.greeting_label.pack(side='left')

        self.time_label = ttk.Label(header_frame, text="", font=('Arial', 12))
        self.time_label.pack(side='right', padx=10)
        self.date_label = ttk.Label(header_frame, text="", font=('Arial', 12))
        self.date_label.pack(side='right')

        ttk.Label(header_frame, text="Select Date:", foreground='black', background='#FF5F1F').pack(side='right', padx=(0, 5))
        self.date_entry = DateEntry(header_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.set_date(controller.selected_date)
        self.date_entry.pack(side='right', padx=(0, 10))
        self.date_entry.bind("<<DateEntrySelected>>", self.on_date_change)

        button_area = ttk.Frame(self, padding="40")
        button_area.pack(pady=50, padx=50)

        ttk.Label(button_area, text="SELECT CUSTOMER SEGMENT (RFM Cluster)",
                  font=('Arial', 16, 'bold'), foreground='#000000').grid(row=0, column=0, columnspan=5, pady=(0, 30))

        segment_names = {-1: "Initial", 0: "Steady", 1: "Emerging", 2: "Mature", 3: "Leading"}

        for i, cluster_id in enumerate(self.controller.cluster_summary.keys()):
            row = i // 3 + 1
            col = i % 3
            ttk.Button(button_area, text=segment_names.get(int(cluster_id), f"Cluster {cluster_id}"),
                       style='Accent.TButton', width=25,
                       command=lambda c=int(cluster_id): controller.show_frame("ClusterDetailPage", c)
                       ).grid(row=row, column=col, padx=20, pady=20, sticky='ew')

        self.update_clock_and_greeting()

    def update_clock_and_greeting(self):
        now = datetime.datetime.now()
        date_str = self.controller.selected_date.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        self.date_label.config(text=date_str)
        self.time_label.config(text=time_str)

        
        event_today = get_event_for_date(self.controller.selected_date)
        if event_today:
            greeting_text = f"Happy {event_today}, {ADMIN_NAME}!"
        else:
            hour = now.hour
            if 5 <= hour < 12:
                greeting_text = f"Good Morning, {ADMIN_NAME}!"
            elif 12 <= hour < 17:
                greeting_text = f"Good Afternoon, {ADMIN_NAME}!"
            else:
                greeting_text = f"Good Evening, {ADMIN_NAME}!"
        self.greeting_label.config(text=greeting_text)

        self.after(1000, self.update_clock_and_greeting)

    def on_date_change(self, event):
        selected_date = self.date_entry.get_date()
        current_time = datetime.datetime.now().time()
        self.controller.selected_date = datetime.datetime.combine(selected_date, current_time)


class ClusterDetailPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_cluster_id = None

        back_frame = ttk.Frame(self, padding="10")
        back_frame.pack(fill='x')
        ttk.Button(back_frame, text="< Back to Dashboard", command=lambda: controller.show_frame("HomePage")).pack(side='left')

        self.title_label = ttk.Label(self, text="Segment: ", style='Header.TLabel', anchor='center')
        self.title_label.pack(pady=10)

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill='both', expand=True)

        metrics_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        metrics_frame.pack(side='left', fill='y', padx=20, pady=10)

        ttk.Label(metrics_frame, text="Cluster Performance Summary", style='CardHeader.TLabel').pack(pady=10)
        self.customer_count_label = ttk.Label(metrics_frame, text="Total Customers: N/A", style='Text.TLabel', font=('Arial', 14))
        self.customer_count_label.pack(pady=10)
        self.revenue_label = ttk.Label(metrics_frame, text="Total Revenue: N/A", style='Text.TLabel', font=('Arial', 14))
        self.revenue_label.pack(pady=10)

        self.insights_button = ttk.Button(metrics_frame, text="INSIGHTS", style='Accent.TButton', width=25)
        self.insights_button.pack(pady=(20, 0))

        offers_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        offers_frame.pack(side='right', fill='both', expand=True, pady=10)

        ttk.Label(offers_frame, text="Proposed Marketing Strategy", style='CardHeader.TLabel').pack(pady=10)
        ttk.Label(offers_frame, text="Strategic Goal:", style='Text.TLabel', foreground='#F39C12').pack(anchor='w', pady=(10, 0))

        self.goal_text = tk.Text(offers_frame, height=3, width=60, font=('Arial', 10),
                                 wrap='word', bg='#2C3E50', fg='#ECF0F1', borderwidth=0)
        self.goal_text.pack(pady=(0, 20), fill='x')
        self.goal_text.config(state='disabled')

        ttk.Label(offers_frame, text="Select Offer to Send:", style='Text.TLabel', foreground='#F39C12').pack(anchor='w', pady=(10, 0))
        self.offer_var = tk.StringVar()
        self.offer_combobox = ttk.Combobox(offers_frame, textvariable=self.offer_var, state='readonly',
                                           width=50, font=('Arial', 10))
        self.offer_combobox.pack(pady=(0, 10), anchor='w')

        self.send_button = ttk.Button(offers_frame, text="GENERATE & SEND MESSAGE", style='Accent.TButton',
                                      width=40, command=self.generate_message)
        self.send_button.pack(pady=20)

        self.loading_label = ttk.Label(offers_frame, text="", foreground='#58D68D')
        self.loading_label.pack()

        self.insights_button.config(command=self.show_insights)

    def update_display(self, cluster_id):
        self.current_cluster_id = cluster_id
        data = self.controller.get_summary_for_cluster(cluster_id)
        logic = OFFER_PROPOSALS.get(cluster_id, OFFER_PROPOSALS[-1])

        self.title_label.config(text=f"Segment: {logic['segment'].split('(')[0].strip()}")
        self.customer_count_label.config(text=f"Total Customers: {data['customers']:,}")
        self.revenue_label.config(text=f"Total Revenue: ₹{data['revenue']:,.2f}")

        self.goal_text.config(state='normal')
        self.goal_text.delete('1.0', tk.END)
        self.goal_text.insert(tk.END, logic['goal'])
        self.goal_text.config(state='disabled')

        self.offer_combobox['values'] = logic['offers']
        if logic['offers']:
            self.offer_combobox.set(logic['offers'][0])

    def show_insights(self):
        cluster_id = self.current_cluster_id
        visuals_folder = os.path.join(
            r"C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\P1\visuals",
            f"cluster_{cluster_id}"
        )

        if not os.path.exists(visuals_folder):
            messagebox.showerror("Error", f"No visuals found for cluster {cluster_id}")
            return

        VisualsViewerWindow(self.controller, visuals_folder, cluster_id)

    def generate_message(self):
        if self.current_cluster_id is None:
            messagebox.showwarning("Select Cluster", "Please select a cluster first.")
            return
        offer_selected = self.offer_var.get()
        logic = OFFER_PROPOSALS.get(self.current_cluster_id, OFFER_PROPOSALS[-1])
        event_today = get_event_for_date(self.controller.selected_date)

        self.loading_label.config(text="Generating message...")
        self.update()

        
        sms_result = generate_ollama_message(self.current_cluster_id, offer_selected, logic, event_today)


        if not sms_result or 'error' in sms_result:
            messagebox.showerror("Error", sms_result.get('error', 'Failed to generate message'))
            self.loading_label.config(text="")
            return

        sms_copy = sms_result.get('sms_copy', '')
        self.loading_label.config(text="Message generated!")

        
        if not self.controller.phone_mockup_window or not self.controller.phone_mockup_window.winfo_exists():
            self.controller.phone_mockup_window = PhoneMockup(master=self.controller)
        self.controller.phone_mockup_window.update_message(sms_copy)
        self.controller.phone_mockup_window.deiconify()  

if __name__ == '__main__':
    app = MarketingApp()
    app.mainloop()
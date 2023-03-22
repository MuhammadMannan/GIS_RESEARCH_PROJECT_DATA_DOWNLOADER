import tkinter as tk
import tkinter.ttk as ttk
import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class DataDownloaderGUI:
    def __init__(self, master):
        # set up the window
        self.master = master
        self.master.title("Data Downloader")

        # initialize Firebase credentials
        cred = credentials.Certificate('uw-gis-project-firebase-adminsdk-qai1z-404da4088d.json')
        firebase_admin.initialize_app(cred)
        
        # initialize Firestore client
        self.db = firestore.client()
        
        # define the collection and document to retrieve data from
        self.collection_name = 'plants'
        
        # create the treeview to display the data
        self.treeview = ttk.Treeview(self.master)
        self.treeview.pack(side="left", fill="both", expand=True)

        # create the scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")

        # configure the treeview to use the scrollbar
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # define the output file name
        self.output_file = 'output.csv'

        # create the button to download the data
        self.download_button = tk.Button(self.master, text="Load Data", command=self.download_data)
        self.download_button.pack(pady=10)

    def download_data(self):
        # retrieve all documents in the collection
        docs = self.db.collection(self.collection_name).stream()

        # save data to CSV file
        with open(self.output_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            # write the headers
            headers_written = False
            
            # loop over all documents in the collection
            for doc in docs:
                # get the data from the current document
                data = doc.to_dict()
                
                # write the headers if not yet written
                if not headers_written:
                    writer.writerow(data.keys())
                    headers_written = True
                
                # write the data
                writer.writerow(data.values())

        # display the data in the treeview
        with open(self.output_file, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames
            self.treeview["columns"] = headers
            self.treeview.heading("#0", text="Index")
            for header in headers:
                self.treeview.heading(header, text=header)
            for i, row in enumerate(reader, 1):
                self.treeview.insert(parent="", index="end", iid=i, text=str(i), values=[row[header] for header in headers])

if __name__ == "__main__":
    root = tk.Tk()
    app = DataDownloaderGUI(root)
    root.mainloop()

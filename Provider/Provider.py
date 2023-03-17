import json
from Member import *
from Service import *
import random
import os
from pathlib import Path
import shutil
import pandas as pd
from tabulate import tabulate
from datetime import date, timedelta, datetime
import sys



class Provider:
    def __init__(self):
        self.provider_id = ""
        self.provider_name = None
        self.strAddr = ""
        self.city = ""
        self.state = ""
        self.zip = ""
        self.removal_date = "" #added for remove/will need to change test file
        #do we need a provider status change date member? to test removal
    
    def enter_Provider_details(self):
        print("Please enter provider's name: ")
        self.provider_name = input("> ")
        for i in range(9):
            self.provider_id += str(random.randint(0,9))
        print("Please enter the Street Address: ")
        self.strAddr = input("> ")
        print("Please enter the City: ")
        self.city = input("> ")
        while not self.city.isalpha():
            print("Not a valid city, try again.")
            self.city = input("Please enter a valid city: ")
        print("Please enter the State: ")
        self.state= input("> ")
        while len(self.state) != 2 or (not self.state.isalpha()):
            print("Not a valid state, try again.")
            self.state = input("Please enter a valid state: ")
        print("Please enter the zipcode: ")
        self.zip = input("> ")
        while len(self.zip) != 5 or (not self.zip.isdigit()):
            print("Not a 5 digit number, try again.")
            self.zip = input("Please enter your 5 digit zipcode: ")
            
        self.removal_date = "Active" # Added for removal, will need to change test file
        self.add_provider()
    
    def print_exists(self):
        print("Provider already exists.") 
    
    def print_not_found(self):
        print("Provider does not exist.")
         
    #test
    def add_provider(self):

        cwd = os.getcwd() #gets current working directory
        parent_dir = "Provider" #sets relative path in variable
        
        #If provider already has a file, will print a statement that it exists
        if os.path.exists(f"{cwd}/{parent_dir}/{self.provider_name}"): 
            self.print_exists()

        else:
            #Creates the new provider directory
            directory = f"{self.provider_name}/" #new provider directory
            path = os.getcwd() + "/Provider/" + directory  #sets path to the new provider's directory
            os.makedirs(path)
            #Contents for file that is uploaded
            provider = {
                    "ProviderName": self.provider_name,
                    "ProviderID": self.provider_id,
                    "ProviderRemoval": self.removal_date, # Added for removal, will need to change test file
                    "ProviderAddr": self.strAddr,
                    "ProviderCity": self.city,
                    "ProviderState": self.state,
                    "ProviderZip": self.zip,
                    "Services": [
                        
                    ],
                    "TotalConsultations": 0,
                    "TotalFee": "$0.00"
            }
            #Opens the path to the new folder and creates new json file for provider profile        
            #with open(f"{path}/{self.provider_name}_{str(today)}.json",mode="w") as file:   #file 
             #  json.dump(provider,file,indent= 4)
            with open(f"{path}/{self.provider_name}_profile.json",mode="w") as file:   #file  
               json.dump(provider,file,indent= 4)

            #Opens the path to the Provider folder for the
            # list of providers in the json file
            
            with open(f"{cwd}/{parent_dir}/ProviderList.json",mode="r") as file:
                data = json.load(file)
                
            #New provider data for the json file containing all providers in Provider folder
            new_provider = {
                "ProviderName": self.provider_name,
                "ProviderId": self.provider_id,
                "ProviderRemoval": self.removal_date, # Added for removal, will need to change test file
            }
            #Appends the new provider to the full provider list
            data['providers'].append(new_provider)
            with open(f"{cwd}/{parent_dir}/ProviderList.json",mode="w") as file:
                json.dump(data,file,indent=4)

        options = {
                'Options': ['1. Add Another Provider', '2. Return to Main Menu']
            }
        df = pd.DataFrame(options)
        df_styled = df.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]).set_properties(**{'text-align': 'left'})
        print(tabulate(df_styled.data, headers=df_styled.columns, tablefmt='fancy_grid', showindex=False))
        ch = int(input("Please enter your choice: "))
        if ch == 1:
            self.enter_Provider_details()
            
    def remove_provider(self):
        self.display_providers()
        found = False
        id = self.getProviderID()
        pName = self.getProviderName(id, 0)
        pRemove = self.getProviderRemoval(id)
        if pName != None:
            found = True
            path = os.getcwd() + '/Provider/' + pName
            print(path)
            if pRemove == "Active":
            #self.removal_date = date.today() #sets removal date to today
                with open(f"{path}/{pName}_profile.json",mode="r") as file:   #file 
                    data = json.load(file)
                data["ProviderRemoval"] = str(date.today())
                with open(f"{path}/{pName}_profile.json",mode="w") as file:   #file 
                    json.dump(data,file,indent=4)
                with open("Provider/ProviderList.json",mode="r") as file:   #file 
                    data = json.load(file)
        
                for provider in data["providers"]:
                    if provider["ProviderName"] == pName:
                        provider["ProviderRemoval"] = str(date.today())
                    with open("Provider/ProviderList.json",mode="w") as file:
                        json.dump(data,file,indent=4)
            elif datetime.strptime(pRemove, '%Y-%m-%d').date() + timedelta(days=8) < date.today():
                #self.full_removal(path)
                shutil.rmtree(path)
                with open("Provider/ProviderList.json",mode="r") as file:
                    data = json.load(file)
                for index,provider in enumerate(data['providers']):
                    if provider['ProviderId'] == id:
                        data['providers'].pop(index)
                        found = True
                with open("Provider/ProviderList.json",mode="w") as file:
                    json.dump(data,file, indent = 4)    
            # return found
        else:
            self.print_not_found()
        
    def update_Pmenu(self):
        print("To update name, enter 1")
        print("To update address, enter 2")
        choice = input()
        return choice

    #Get updated name
    def ask_name(self):
        print("Write the updated name of the provider: ")
        new_pName = input()
        return new_pName
  
    
    #Update the Provider profile & info in ProviderList
    def update_provider(self):
        id = self.getProviderID()
        pName = self.getProviderName(id, 0)
        if pName == None:
                return
        choice = self.update_Pmenu()
        path = os.getcwd() + '/Provider/' + pName #Go to the dir
        if(os.path.exists(path)):
            if choice == "1": #Update Provider Name
                self.provider_name = new_name = self.ask_name()    # Need edit function to call
                new_path = os.getcwd() + '/Provider/' + new_name
                os.rename(f"{path}/{pName}_profile.json", f"{path}/{new_name}_profile.json") #Renaming Profile
                shutil.move(path, new_path) #Move the dir & contents to new_named dir

                #Need to edit the dictionary now
                with open(f"{new_path}/{new_name}_profile.json",mode="r") as file:   #file 
                    data = json.load(file)
                data["ProviderName"] = new_name
                with open(f"{new_path}/{new_name}_profile.json",mode="w") as file:   #file 
                    json.dump(data,file,indent=4)
                with open("Provider/ProviderList.json",mode="r") as file:   #file 
                    data = json.load(file)

                for provider in data["providers"]:
                    if provider["ProviderName"] == pName:
                        provider["ProviderName"] = new_name
                with open("Provider/ProviderList.json",mode="w") as file:
                        json.dump(data,file,indent=4)
            
            elif choice == "2": #Update Provider Address
                print("Please enter the updated Street Address: ")
                new_StrAdd = input("> ")
                print("Please enter the updated City: ")
                new_city = input("> ")
                print("Please enter the updated State: ")
                new_state= input("> ")
                print("Please enter the updated zipcode: ")
                new_zip = input("> ")
                with open(f"{path}/{pName}_profile.json",mode="r") as file:   #file 
                        data = json.load(file)
                data["ProviderAddr"] = new_StrAdd
                data["ProviderCity"] = new_city
                data["ProviderState"] = new_state
                data["ProviderZip"] = new_zip
                with open(f"{path}/{pName}_profile.json",mode="w") as file:   #file 
                        json.dump(data,file,indent=4)

            else:
                print("Invalid option!")
                self.update_provider()
        else:
            self.print_not_found()


    #Just a print statement to reuse in multiple functions
    def ask_for_ID(self):
        print("Please enter a valid provider ID number: ")
    
    def getProviderID(self):
        self.ask_for_ID()

        id = input("> ")
        if len(id) != 9 or id.isnumeric() == False:
            return self.getProviderID()
        return id  
        
    def printWelcomeMessage(self, name):
        print("Welcome ", name)
        
    def getProviderRemoval(self, id):
        with open("Provider/ProviderList.json",mode="r") as file:
            data = json.load(file)
        for member in data['providers']:
            if member['ProviderId'] == id:
                removal_date = member["ProviderRemoval"]
                return removal_date
        return None  
    
    #test
    def getProviderName(self,id, choice):
        with open("Provider/ProviderList.json",mode="r") as file:
            data = json.load(file)
        for member in data['providers']:
            if member['ProviderId'] == id:
                name = member["ProviderName"]
                if choice == 1:
                    self.printWelcomeMessage(name)
                return name
        return None
    
    def get_comment(self):
        print("Please enter a comment (100 characters): ")
        comment = input('> ')
        if len(comment) > 100:
            print('Your comment surpassed 100 characters.\nPlease Redo!')
            return self.get_comment()
        else:
            return comment

    def add_comments(self, provider_name):
        print("Would you like to enter comments about the service provided? [y/n]")
        ans2 = input("> ")
        if ans2 == 'y':
            comment = self.get_comment()
            return comment
        return "No Comments Provided"
    
    def load_validated(self, provider_id,provider_name, date_of_service, member_id,member_name):  
        s = Service()
        
        print("Please enter service code:")
        service_code = input("> ")
        validServiceCode = False
        with open("Service/ProviderDirectory.json") as file:
            data = json.load(file)
        for service in data['services']:
            if service['serviceCode'] == service_code:
                sname = service['serviceName']
                validServiceCode = True
                s.printServiceName(sname)
                s.validateServiceName(sname, provider_id,provider_name, member_id,member_name, date_of_service)
                break
        if(validServiceCode == False):
            print("Invalid service code")
            self.load_validated(provider_name, date_of_service, member_name)
            
    def get_date_service(self, provider_id,provider_name, member_id,member_name):
        print("\nPlease enter the date the service was provided. ")
        year = int(input('Enter year (yyyy): '))
        month = int(input('Enter month (mm): '))
        day = int(input('Enter day (dd): '))

        d = date(year, month, day)
      
        if date.today() < d:
            print("Invalid Date!")
            self.get_date_service(provider_id,provider_name,member_id,member_name)
        elif date.today() - timedelta(days=6) > d:
            print("Invalid Date!")
            self.get_date_service(provider_id,provider_name,member_id,member_name)
        else:
            self.load_validated(provider_id,provider_name, d, member_id,member_name)
        
    def load(self):
        # gets provider id & name
        while(self.provider_name == None):
            print("Enter Valid Provider Id")   
            self.provider_id = self.getProviderID()
            self.provider_name = self.getProviderName(self.provider_id, 1)
       
        # gets member id & name
        m = Member()
        while(m.member_name == None):
            print("Enter Valid Member Id")  
            m.member_id = m.getMemberID()
            m.member_name = m.getMemberName(m.member_id)

        # checks for member account status
        if m.validate_member(m.member_id) == True: 
            if m.isSuspended(m.member_id) == True:
                m.printSuspended()
            else:
                print("Validated")
                self.get_date_service(self.provider_id,self.provider_name,m.member_id, m.member_name)
        

    def display_providers(self):
        with open('Provider/ProviderList.json') as f:
            data = json.load(f)

        # Extract fields
        rows = []
        for obj in data['providers']:
            rows.append([obj['ProviderName'], obj['ProviderId']])

        # Print table
        headers = ['Name', 'ID']
        print(tabulate(rows, headers=headers))
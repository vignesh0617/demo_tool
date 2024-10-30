import os

print("Going to install required packages .....")

try:
    #os.system('pip install mysql-connector-python')
    os.system('pip install -r requirements.txt')
except Exception as e:
    print(f'''\n\n\n
      ********************************************************************
      *---------------------------Error!!---------------------------------*
      ********************************************************************
      \n\n\n''')
    input(e,"\n\n\nClick any button to exit")
    

input(f'''\n\n\n
      ********************************************************************
      *-----Required packages installed. Click any button to exit--------*
      ********************************************************************
      \n\n\n''')

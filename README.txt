PreRequisited to run CIDM :
---------------------------
	1) MySQL workbench 8.0 or greater version needs to be installed
	2) Python version 3.10 or greater version needs to be installed

Once the above two conditions are satisfied:

	3) Run "installation.py"
	4) Change the following properties in app/environment.txt as per your requirements
			database_name = <your database/schema name>
			username = <your user name>
			password = <your password>
	5) Then run "main_app.py" in app/main_app.py to use CIDM.
	6) Now you can access CIDM in any browser by using the address : "http://127.0.0.1:8052/login"

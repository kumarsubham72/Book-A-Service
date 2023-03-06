from flask import Flask,render_template,request,redirect,url_for,session
import pyodbc 
from geopy import distance
from geopy.geocoders import Nominatim
import smtplib

#connecting Database 
server = 'abhyudai.database.windows.net'
database = 'abhyudai'
username = 'abhyudai'
password = 'HR26m1239#'


# {ODBC Driver 17 for SQL Server}
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


app = Flask(__name__,template_folder='templates')
app.secret_key= 'hello'


global useremail #user email has been declared globally 
useremail = " abhyudai "
global vendiorloginemail 
vendiorloginemail = "abhyudai"
global vendorloginemail # verdaor email has been declared globally 
global SR 



#to reach home page directly 
@app.route("/",methods=["POST", "GET"])
def homepage():
    return render_template('homepage.html')

#to reach register page via navbar 
@app.route("/Register",methods=["POST", "GET"])
def Register():
    return render_template('Signup.html')

#for vendor to register 
@app.route("/VendorRegister",methods=["POST", "GET"])
def VendorRegister():
    return render_template('Vendorsignup.html')

#for vendor login
@app.route("/VendorLogin",methods=["POST", "GET"])
def VendorLogin():
    return render_template('Vendorlogin.html')

#to reach login page via navbar 
@app.route("/Login",methods=["POST", "GET"])
def Login():
    return render_template('login.html')

#search for service categories 
@app.route("/Search",methods=["POST", "GET"])
def Search():
     if request.method == 'POST':
        details = request.form
        search = (details['Search'])
        cursor.execute("select email,FirstName,ServiceCategory, servicetype, Price from vendorsignup where servicetype LIKE  '"+ search +"';")
        vendor_details = cursor.fetchall()
        return render_template('servicerequest.html',vendor_details=vendor_details)

#Contact support page 
@app.route("/Contactsupport",methods=["POST", "GET"])
def Contactsupport():
    return render_template('contact.html')

#to reach about page  
@app.route("/About",methods=["POST", "GET"])
def About():
    return render_template('about.html')

#getting details from the data base and pay option 
@app.route("/Myservicerequest",methods=["POST", "GET"])
def Myservicerequest():
    if "useremail" in session:
        useremail = session["useremail"]
        print(useremail)
        cursor = cnxn.cursor()
        cursor.execute("select email,name,ServiceCategory, servicetype, price,status,useremail,SR from servicerequest where useremail = '"+ useremail +"';")
        servicerequest_details  = cursor.fetchall()
        print(servicerequest_details)
        return render_template('Myservicerequest.html',servicerequest_details=servicerequest_details)

#Electrical Service Page
@app.route("/ElectricalService",methods=["POST", "GET"])
def ElectricalService():
    return render_template('ElectricalService.html')

#Plumbing Service Page
@app.route("/PlumbingService",methods=["POST", "GET"])
def PlumbingService():
    return render_template('PlumbingService.html')

#Pest Control Service Page
@app.route("/PestControlService",methods=["POST", "GET"])
def PestControlService():
    return render_template('PestControlService.html')

#Appliances Service Page
@app.route("/AppliancesService",methods=["POST", "GET"])
def AppliancesService():
    return render_template('AppliancesService.html')

#Home Cleaning Service Page
@app.route("/HomeCleaningService",methods=["POST", "GET"])
def HomeCleaningService():
    return render_template('HomeCleaningService.html')


#to signup page and enter details to database  from the navbar 
@app.route("/Signup",methods=["GET", "POST"])
def Signup():
    if request.method == 'POST':
        details = request.form
        email = (details['Email'])
        psw = (details['Psw'])
        firstname = (details['Firstname'])
        print(firstname)
        lastname = (details['LastName'])
        print(lastname)
        apartment = (details['Apartment'])
        street = (details['Street'])
        city = (details['City'])
        state = (details['State'])
        country = (details['Country'])
        zip = (details['ZIP'])
        mobile = (details['Mobile'])
        user_address = street+ " " + city + " " + state + " " + country 
        print(user_address)
        user_address_location = Nominatim(user_agent='tutorial').geocode(user_address)
        print(user_address_location)
        if user_address_location == None: 
            return render_template('No_usersignup.html')
        else:
            user_address_latitude = str(user_address_location.latitude) 
            user_address_longitude = str(user_address_location.longitude) 
            print(user_address_latitude)
            print(user_address_longitude)
            cursor = cnxn.cursor()
            cursor.execute(" INSERT INTO usersignup  (email, psw,FirstName, LastName, apartment, street, city, state, country, ZIP, mobile,latitude,longitude) VALUES ('"+ email +"', '"+ psw +"','"+ firstname +"','" + lastname + "','" + apartment +"', '" + street +"','" + city +"', '" + state +"','" + country +"','" + zip +"','" + mobile + "','" + user_address_latitude  + "','" + user_address_longitude + "');")
            cursor.connection.commit()
            cursor.execute("select FirstName,LastName from usersignup where email like '"+ email +"';")
            user_names = cursor.fetchone()
            first_Name= user_names[0] 
            last_Name = user_names[1]
            return render_template('loginhomepage.html',First_Name = first_Name,Last_Name= last_Name)
    return render_template('homepage.html')

#vendor signup from footer 
@app.route("/VendorSignup",methods=["POST", "GET"])
def VendorSignup():
    if request.method == 'POST':
        details = request.form
        vendoremail = (details['VendorEmail'])
        psw = (details['VendorPsw'])
        firstname = (details['VendorFirstName'])
        lastname = (details['VendorLastName'])
        vendorapartment = (details['VendorApartment'])
        street = (details['VendorStreet'])
        city = (details['VendorCity'])
        state = (details['VendorState'])
        country = (details['VendorCountry'])
        zip = (details['VendorZIP'])
        mobile = (details['VendorMobile'])
        servicecategory = details['VendorServiceCategory']
        servicetype = details['VendorServicetype']
        price = details['Price']
        vendor_address = street+ " " + city + " " + state + " " + country
        vendor_address_location= Nominatim(user_agent='tutorial').geocode(vendor_address)
        print(vendor_address_location)
        if vendor_address_location == None:
            return render_template ('No_vendorsignup.html')
        else:    
            user_address_latitude = str(vendor_address_location.latitude) 
            user_address_longitude = str(vendor_address_location.longitude) 
            print(user_address_latitude)
            print(user_address_longitude)
            servicecategory=(details['VendorServiceCategory'])
            servicetype=(details['VendorServicetype'])
            cursor = cnxn.cursor()
            ####  change table name 
            cursor.execute(" INSERT INTO vendorsignup  (email, psw,FirstName,LastName, apartment,street, city, state, country, ZIP, mobile, serviceCategory, servicetype,latitude,longitude,Price) VALUES ('"+ vendoremail +"', '"+ psw +"','"+ firstname +"','"+ lastname +"', '"+ vendorapartment +"','"+ street +"','"+ city +"', '"+ state +"','"+ country +"','"+ zip +"','"+ mobile +"','"+ servicecategory +"','"+ servicetype +"','"+ user_address_latitude +"','"+ user_address_longitude +"','"+ price +"');")
            #cursor.execute(" INSERT INTO vendorsignup  (email, psw,FirstName,LastName, apartment,street, city, state, country, ZIP, mobile, serviceCategory, servicetype,latitude,longitude) VALUES ('"+ vendoremail +"', '"+ psw +"','"+ firstname +"','"+ lastname +"', '"+ vendorapartment +"','"+ street +"','"+ city +"', '"+ state +"','"+ country +"','"+ zip +"','"+ mobile +"','"+ servicecategory +"','"+ servicetyoe +"','"+ user_address_latitude +"','"+ user_address_longitude +"');")
            cursor.connection.commit()
            cursor.execute("SELECT FirstName, LastName from vendorsignup where email LIKE '"+ vendoremail +"';")
            user_names = cursor.fetchone()
            first_Name= user_names[0] 
            last_Name = user_names[1]
            return render_template ('vendorloginhomepage.html',First_Name = first_Name,Last_Name= last_Name)
    return render_template('homepage.html')


#login page from the navbar 
@app.route("/Loginverify",methods=["POST", "GET"])
def Loginverify():
    if request.method == 'POST':
        details = request.form
        useremail = (details['LoginEmail'])
        print(useremail)
        session ['useremail'] = useremail
        loginPsw = (details['LoginPsw'])
        login_check = []
        cursor = cnxn.cursor()
        cursor.execute("select email,psw from usersignup where email like '"+ useremail +"';")
        login_check = cursor.fetchone()
        print(login_check[1])
        if login_check[1] == loginPsw:
            cursor.execute("select FirstName,LastName from usersignup where email like '"+ useremail +"';")
            user_names = cursor.fetchone()
            first_Name= user_names[0] 
            last_Name = user_names[1]
            return render_template('loginhomepage.html', First_Name = first_Name,Last_Name= last_Name)
        else:

            return render_template('No_loginhomepage.html')


@app.route("/Bookservice", methods=['POST', 'GET'])
def Bookservice():
    if request.method == 'POST':
        details = request.form
        servicecategory=(details['servicecategorytag'])
        servicetype = (details['servicetypetag'])
        print(servicecategory)
        print(servicetype)
        if "useremail" in session:
            useremail = session["useremail"]
            print(useremail)
            cursor = cnxn.cursor()
            cursor.execute("select latitude, longitude from usersignup where email like '"+ useremail +"';")
            lat_long= cursor.fetchone()
            user_lat = lat_long[0]
            user_long= lat_long[1]
            user_coord = user_lat,user_long
            print(user_coord,"User coord")
            vendor_lat_long=[]
            cursor = cnxn.cursor()
            cursor.execute("select latitude, longitude from vendorsignup where servicetype = '"+ servicetype +"';")
            vendor_lat_long = cursor.fetchall()
            vendor_lat_long_str = str(vendor_lat_long)
            vendor_coord=[]
            vendor_coord.append(vendor_lat_long_str)
            print(vendor_coord)
            print('#'*50)
            # vendor_distance=[]
            # for i in (vendor_lat_long):
            #     vendor_user_distance= int(distance.distance(user_coord,(i[0],i[1])).miles)
            #     vendor_distance.append(vendor_user_distance)
            #     print(vendor_distance)
            cursor.execute("select email,FirstName,ServiceCategory, servicetype, Price from vendorsignup where servicetype = '"+ servicetype +"';")
            vendor_details = cursor.fetchall()
            print(vendor_details)
            return render_template('servicerequest.html',vendor_details= vendor_details)


#Vendor login page from the footer 
@app.route("/VendorLoginverify",methods=["POST", "GET"])
def VendorLoginverify():
    if request.method == 'POST':
        details = request.form
        vendiorloginemail = (details['VendorLoginEmail'])
        session ['vendiorloginemail'] = vendiorloginemail
        print(vendiorloginemail)
        vendorloginPsw = (details['VendorLoginPsw'])
        print(vendorloginPsw)
        login_check = []
        cursor = cnxn.cursor()
        cursor.execute("select email,psw from vendorsignup where email like '"+ vendiorloginemail +"';")
        login_check = cursor.fetchone()
        print(login_check[1])
        if login_check[1] == vendorloginPsw:
            cursor.execute("select FirstName,LastName from vendorsignup where email like '"+ vendiorloginemail +"';")
            user_names = cursor.fetchone()
            first_Name= user_names[0] 
            last_Name = user_names[1]
            cursor.execute("select email,name,ServiceCategory, servicetype, Price,status,SR from servicerequest where email = '"+ vendiorloginemail +"';")
            vendorsr_details = cursor.fetchall()
            return render_template('vendorloginhomepage.html', First_Name = first_Name,Last_Name= last_Name,vendorsr_details=vendorsr_details)
    return render_template('No_vendorloginhomepage.html')



#select vendor and service request created 
@app.route("/SelectVendor",methods=["POST", "GET"])
def SelectVendor():
    if request.method == 'POST':
        details = request.form
        email = details['Email']
        name = details['Name']
        servicecategory = details['ServiceCategory']
        servicetype = details['servicetype']
        price = details['Price']
        status = "Requested"
        SR_list=[]
        print(email,name,servicecategory,servicetype,price)
        if "useremail" in session:
            useremail = session["useremail"]
            print(useremail)
            cursor = cnxn.cursor()
            cursor.execute("select SR from servicerequest order by SR DESC;")
            SR= cursor.fetchone()
            # print(SR)
            SR_list = [x for x in SR]
            # print(SR_list)
            SR_Increment = int(SR_list[0]) + 1
            print('#'*50)
            print(SR_Increment)
            print('#'*50)
            SR_Increment_str = str(SR_Increment)
            print(type(SR_Increment_str))
            cursor.execute("INSERT INTO servicerequest (email, name , servicecategory, servicetype,price,status,useremail,SR) VALUES ('"+ email +"', '"+ name +"', '"+ servicecategory +"', '"+ servicetype +"','"+ price +"','"+ status +"','"+ useremail +"','"+ SR_Increment_str +"');")
            cursor.commit()
            cursor.execute("select email,name,ServiceCategory, servicetype, Price,status,SR from servicerequest where useremail = '"+ useremail +"';")
            SR_details = cursor.fetchall()
            return render_template('servicerequested.html',SR_details=SR_details)


        
@app.route("/AcceptSR",methods=["POST", "GET"])
def AcceptSR():
    if request.method == 'POST':
        details = request.form
        email = details['Email']
        name = details['Name']
        servicecategory = details['ServiceCategory']
        servicetype = details['servicetype']
        price = details['Price']
        SR = details['SR']
        status = "Accepted"
        print(email,name,servicecategory,servicetype,price,SR)
        if "useremail" in session:
            useremail = session["useremail"]
            print("#"*20)
            print(useremail)
            print("#"*20)
            cursor.execute("INSERT INTO servicerequest (email, name , servicecategory, servicetype,price,status,useremail,SR) VALUES ('"+ email +"', '"+ name +"', '"+ servicecategory +"', '"+ servicetype +"','"+ price +"','"+ status +"','"+ useremail +"','"+ SR +"');")
            cursor.commit()
            return render_template('vendorloginhomepage.html')


        
@app.route("/ordersummary",methods=["POST", "GET"])
def ordersummary():
    if request.method == 'POST':
        details = request.form
        email = details['Email']
        name = details['Name']
        servicecategory = details['ServiceCategory']
        servicetype = details['servicetype']
        price = details['Price']
        status = details['Status']
        user_email = details['Useremail']
        SR = details['SR']
        session['SR'] = SR
        userdetails_list = []
        cursor.execute("select FirstName,apartment,street,city,state,country,mobile from usersignup where email = '"+ user_email +"'; ")
        userdetails = cursor.fetchone()
        userdetails_list.append(userdetails)
        cursor.execute("select FirstName from usersignup where email = '"+ user_email +"'; ")
        userdetails_name = cursor.fetchone()
        return render_template('ordersummary.html',userdetails=userdetails,userdetails_name= userdetails_name,email=email,name=name,servicecategory=servicecategory,servicetype=servicetype,price=price,status=status,SR=SR)

@app.route("/updatebid",methods=["POST", "GET"])
def updatebid():
    if request.method == 'POST':
        details = request.form
        bid = details['BID']
        if "vendiorloginemail" in session:
            vendiorloginemail = session["vendiorloginemail"]
            cursor.execute("update vendorsignup set price='"+bid+"' where email = '"+ vendiorloginemail +"';")
            cursor.execute("select email,name,ServiceCategory, servicetype, Price,status,SR from servicerequest where email = '"+ vendiorloginemail +"';")
            vendorsr_details = cursor.fetchall()
            return render_template ('servicerequest.html',vendorsr_details=vendorsr_details)


@app.route("/DeclineSR",methods=["POST", "GET"])
def DeclineSR():
    if request.method == 'POST':
        details = request.form
        sr = details['SR']
        cursor.execute("update servicerequestaccepted set status = 'Rejected' where sr = '"+ sr +"';")
        return render_template ('vendorloginhomepage.html')


@app.route("/payment",methods=["POST", "GET"])
def payment():
    return render_template('payments.html')

@app.route("/review_and_ratings",methods=["POST", "GET"])
def review_and_ratings():
    card_holder_name = request.form.get("card_holder_name")
    phone_number = request.form.get("phone_number")
    email = request.form.get("email")
    card_number = request.form.get("card_number")
    exp_month = request.form.get("exp_month")
    exp_year = request.form.get("exp_year")
    cvv = request.form.get("cvv")
    vendor_name = request.form.get("vendor_name")
    service_type = request.form.get("service_type")
    rating = request.form.get("rating")
    message = request.form.get("message")
    communication = request.form.get("communication")
    order_id = 0
    if card_holder_name is None:
       card_holder_name = "" 
    cursor.execute("INSERT INTO order1(customer_name) values ('"+ card_holder_name+"')")
    cursor.connection.commit()
    cursor.execute("SELECT * FROM order1 where customer_name = '" + card_holder_name +"'")
    cid =cursor.fetchone()[0]
    ccid = str(cid)
    order_id = cid
    cursor.commit()
    if ccid or order_id or card_holder_name or phone_number or email or card_number or exp_month or exp_year or cvv is None:
        if phone_number is  None:
            phone_number = ""
            # print("hello3")
        if email is None:
            email = ""     
            # print("hello4")     
        if card_number is None:
            card_number = "" 
            # print("hello5")   
        if exp_month is None:
            exp_month = ""
            # print("hello6")     
        if exp_year is None:
            exp_year = ""   
            # print("hello7") 
        if cvv is None:
            cvv = ""     
            # print("hello8")
        if ccid is not None:
            ccid = ""   
            # print("hello9")
       # order_id = card_holder_name = phone_number = email = card_number = exp_month = exp_year = cvv = ""  
        cursor.execute("INSERT INTO payment1 (order_id,card_holder_name, phone_number, email, card_number, exp_month,exp_year,cvv) values ('"+ccid+"','"+ card_holder_name+"','"+ phone_number+"','"+ email+"','"+ card_number+"','"+ exp_month+"','" + exp_year+"','"+ cvv+"')")
        cursor.commit()
        if "SR" in session:
            SR = session["SR"]    
            if communication == "on":
                emailmessage = "Hi "  + card_holder_name + "\n" + " Your order number is " + SR + ". "  +  "Thank you for shopping with us."
                server = smtplib.SMTP("smtp.gmail.com",587)
                server.starttls()
                server.login("subham.automationanywhere@gmail.com", "xbnrjendzhantdum")
                server.sendmail("email",email,emailmessage)
                return render_template("reviewrating.html", card_holder_name = card_holder_name ,phone_number = phone_number ,vendor_name = vendor_name )


@app.route("/reviewupdate",methods=["POST", "GET"])
def reviewupdate():
    rating = request.form.get("rating")
    message = request.form.get("message")
    if "SR" in session:
        SR = session["SR"]   
        cursor.execute(" UPDATE  servicerequest set rating = '"+ rating  +"' , message = '"+ message +"' where SR = '"+ SR +"';")
        cursor.commit()
        return render_template('homepage.html')

if __name__ == "__main__":
    app.run(debug=True)
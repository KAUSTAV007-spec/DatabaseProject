from flask import Blueprint,render_template,request
import cx_Oracle
import pandas as pd
app1=Blueprint("app1",__name__)
con = cx_Oracle.connect(user="system", password="Keira.Knightley")
cur=con.cursor()

@app1.route("/client", methods=['GET', 'POST'])
def clientF():
    return render_template("Client.html")

@app1.route("/ClientL", methods=['GET', 'POST'])
def clientF1():
    try:
        num1=int(request.form['num1'])
    except ValueError:
        return render_template("ValidCreationError.html",result="Improper values provided")
    num1=str(num1)
    num2 = (request.form['num2'])
    str1="select ClientPassword from Client where ClientID="+num1
    cur.execute(str1)
    r=cur.fetchall()
    if(len(r)==0):
     return render_template('Invalid.html')
    elif(num2==r[0][0]):
        str2="select * from (select * from PolicyBought natural join policy) where ClientID="+num1
        cur.execute(str2)
        r1=cur.fetchall()
        df1=pd.DataFrame(r1)
        df1.index+=1
        df1.rename(columns={0:'PolicyBoughtCode',1:'ClientCode',2:'BeneficiaryName',3:'RelationshipWithBeneficiary',4:'PolicyName',5:'PremiumMonthly',6:'AmountOnDeath'},inplace=True)
        return render_template('Result.html',tables=[df1.to_html(classes='data', header="true",justify="center")],titles = ['na', 'ClientDetails'])

    else:
     return render_template("Invalid.html")

@app1.route("/emp", methods=['GET', 'POST'])
def empF():
    return render_template("Emp.html")

@app1.route("/empL", methods=['GET', 'POST'])
def empF1():
    try:
        num1=int(request.form['num1'])
    except ValueError:
        return render_template("ValidCreationError.html",result="Improper values provided")
    num1=str(num1)
    num2 = (request.form['num2'])
    str1="select EmployeePassword from Employee where EmployeeID="+num1
    cur.execute(str1)
    r=cur.fetchall()
    if(len(r)==0):
     return render_template('Invalid.html')
    elif(num2==r[0][0]):
        str2="select designation from Employee where EmployeeID="+num1
        str3="select BranchCode from Employee where EmployeeID="+num1
        cur.execute(str3)
        r=cur.fetchall()
        str4=str(r[0][0])
        cur.execute(str2)
        r=cur.fetchall()
        str5=r[0][0]
        strE="select * from Employee where BranchCode="+str4+"order by EmployeeID desc"
        strA="select * from agent where BranchCode="+str4+"order by AgentID desc"
        strD="select * from client natural join policyBought where BranchCode="+str4+"order by ClientID desc"
        cur.execute(strE)
        r=cur.fetchall()
        df1=pd.DataFrame(r)
        df1.drop(1,axis=1,inplace=True)
        df1.index+=1
        df1.rename(columns={0:'EmployeeID',2:'EmployeeFirstName',3:'EmployeeLastName',4:'Designation',5:'BranchCode'},inplace=True)
        cur.execute(strA)
        r=cur.fetchall()
        df2=pd.DataFrame(r)
        df2.drop(3,axis=1,inplace=True)
        df2.index+=1
        df2.rename(columns={0:'AgentID',1:'AgentFirstName',2:'AgentLastName',4:'BranchCode'},inplace=True)
        cur.execute(strD)
        r=cur.fetchall()
        df4=pd.DataFrame(r)
        df4.drop(1,axis=1,inplace=True)
        df4.index+=1
        df4.rename(columns={0:'ClientID',2:'ClientFirstName',3:'ClientLastName',4:'ClientBranchCode',5:'ClientAgentCode',6:'PolicyCode',7:'Beneficiary',8:'Relationship'},inplace=True)
        if(str5=='CLERK'):
          return render_template('Clerk.html')
        elif(str5=='BM'):
          return render_template('result.html',tables=[df1.to_html(classes='data', header="true",justify="center"),df2.to_html(classes='data', header="true",justify="center"),df4.to_html(classes='data', header="true",justify="center")],titles = ['na', 'Employee','Agent','Client and Policy Information'])
        elif(str5=='AAO'):
          return render_template('result.html',tables=[df2.to_html(classes='data', header="true",justify="center")],titles = ['na','Agent'])
        elif(str5=='AO'):
          return render_template('result.html',tables=[df2.to_html(classes='data', header="true",justify="center"),df4.to_html(classes='data', header="true",justify="center")],titles = ['na','Agent','Client and Policy Information'])
        else:
            return render_template('Invalid.html')


        



    else:
         return render_template('Invalid.html')








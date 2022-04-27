from flask import Flask, render_template, request, jsonify
import cx_Oracle
import pandas as pd
from app1 import app1
from app2 import app2


con = cx_Oracle.connect(user="system", password="Keira.Knightley")
cur=con.cursor()
app = Flask(__name__)
app.register_blueprint(app1)
app.register_blueprint(app2)


@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')
@app.route('/policy', methods=['POST']) 
def policyOperation():
    cur.execute("select *   from policy")
    res = cur.fetchall()
    r=pd.DataFrame(res)
    r.rename(columns={0:'PolicyID',1:'PolicyName',2:'MonthlyPremium',3:'AmountPaidOnDeath'},inplace=True)
    r.index+=1
    cur.execute("select policyID,count(*) from PolicyBought group By policyID ORDER BY count(*) desc")
    r1=cur.fetchall()
    #print(r)
    #print(r1)
    str1="Policies with PolicyID"
    k=0
    for i in r1:
        if(i[1]==r1[0][1]):
            if(k==1):
             str1+=" ,"+str(i[0])
            else:
                 str1+=" "+str(i[0])
                 k+=1
    str1+=" are most sold policies"
    return render_template('result.html',result=str1, tables=[r.to_html(classes='data', header="true",justify="center")],titles = ['na', 'Policies'])

    
    
    
    
    
@app.route('/branch', methods=['POST']) 
def branchLoginOperation():
    return render_template('Branch.html')
@app.route('/BranchL', methods=['POST']) 
def branchLoginOperationC():
    num11=0
    try:
        num11=int(request.form['num1'])
    except ValueError:
        return render_template("ValidCreationError.html",result="Improper values provided")
    num2 = (request.form['num2'])
    num1=str(num11)
    str1="select BranchPassword from Branch where BranchCode="+str(num1)
    cur.execute(str1)
    r=cur.fetchall()
    print(r)
    print(num2)
    if(len(r)==0):
     return render_template('Invalid.html')
    elif(num2==r[0][0]):
        strE="select * from Employee where BranchCode="+num1+"order by EmployeeID desc"
        strA="select * from agent where BranchCode="+num1+"order by AgentID desc"
        strD="select * from client natural join policyBought where BranchCode="+num1+"order by ClientID desc"
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
        print("Good")
        return render_template('Bresult.html',tables=[df1.to_html(classes='data', header="true",justify="center"),df2.to_html(classes='data', header="true",justify="center"),df4.to_html(classes='data', header="true",justify="center")],titles = ['na', 'Employee','Agent','Client and Policy Information'])
    else:
        return render_template('Invalid.html')

if __name__ == '__main__':
    app.run(debug=True)
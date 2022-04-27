from flask import Blueprint,render_template,request
import cx_Oracle
import pandas as pd
app2=Blueprint("app2",__name__)
con = cx_Oracle.connect(user="system", password="Keira.Knightley")
cur=con.cursor()


strg="7"
@app2.route("/agent", methods=['GET', 'POST'])
def agenttF():
    
    return render_template("agent.html")

@app2.route("/agentL", methods=['GET', 'POST'])
def agenttF1():
    try:
        num1=int(request.form['num1'])
    except ValueError:
        return render_template("ValidCreationError.html",result="Improper values provided")
    num1=str(num1)
    num2 = (request.form['num2'])
    str1="select AgentPassword from Agent where AgentID="+num1
    cur.execute(str1)
    r=cur.fetchall()
    if(len(r)==0):
     return render_template('Invalid.html')
    elif(num2==r[0][0]):
        str2="select * from (select * from PolicyBought natural join policy) natural join client where AgentID="+num1
        global strg
        strg=num1
        cur.execute(str2)
        r1=cur.fetchall()
        df1=pd.DataFrame(r1)
        df1.index+=1
        df1.drop(7,axis=1,inplace=True)
        df1.rename(columns={1:'PolicyBoughtCode',0:'ClientCode',2:'BeneficiaryName',3:'RelationshipWithBeneficiary',4:'PolicyName',5:'PremiumMonthly',6:'AmountOnDeath',8:'ClientFirstName',9:'ClientLastName',10:'ClientBranchCode',11:'ClientAgentID'},inplace=True)
        return render_template('Result1.html',tables=[df1.to_html(classes='data', header="true",justify="center")],titles = ['na', 'ClientDetails'])

    else:
     return render_template("Invalid.html")

@app2.route("/branchL2", methods=['GET', 'POST'])
def branchF2():
   
    return render_template("NewPolicy.html")
@app2.route("/branchL3", methods=['GET', 'POST'])
def branchF3():
    
    num2=""
    
    
    num2 = (request.form['num2'])
  
   
    try:
        
        num11=int((request.form['num1']))
        
        num33=int(request.form['num3'])
        
        num44=int(request.form['num4'])

    except ValueError:
        return render_template("ValidCreationError.html",result="Improper values provided")
    str1="select PolicyID from policy where Policyid="+str(num11 )  
    
    cur.execute(str1)
    r1=cur.fetchall()
    print(r1)
    
    if(len(r1)!=0):
        return render_template("InvalidCreation.html")
    else:
       
        if(len(num2)!=0 and num2[0].isalpha() and int(num11)>0 and num33>0 and num44>0 and num44>num33 and num44>=7000) :
            strQ="insert into policy values("+str(num11)+","+"'"+str(num2)+"',"+str(num33)+","+str(num44)+")"
            print(strQ)
            cur.execute(strQ)
            con.commit()
            return render_template("ValidCreationError.html",result="Added Successfully ")
        else:
            return render_template("ValidCreationError.html",result="Improper values provided")

            
    

   
    
        
    

#!/usr/bin/env python                                                                                       
# -*- coding:utf-8 -*-                                                                                      
                                                                                                            
import urllib2
import time
import string
#debug=True                                                                                                 
debug=False
MAXSTOCKNAM = 50
CHECK_MONEYFLOW_ALL_TYPE =0
CHECK_MONEYFLOW_SMALL_TYPE =1
TESTMODE =True   #  是否 是测试模式。  如果真实环境跑， 需要设置为FALSE                                                                                                            
class StockInfo:                                                                                            
    """                                                                                                     
     0: 未知                                                                                                
     1: 名字                                                                                                
     2: 代码                                                                                                
     3: 当前价格                                                                                            
     4: 涨跌                                                                                                
     5: 涨跌%                                                                                               
     6: 成交量（手）                                                                                        
     7: 成交额（万）                                                                                        
     8:                                                                                                     
     9: 总市值"""                                                                                           
                                                                                                            
    def GetStockStrByNum(self,num,type):                                                                              
        try:
          
            #f1= urllib2.Request('http://qt.gtimg.cn/q=s_'+ str(num))
            f1= urllib2.Request('http://qt.gtimg.cn/q='+ str(num))
            f2=urllib2.urlopen(f1)
            #print f2
            print(f2.geturl()) 
            if(debug): print(f2.geturl())                                                                        
            if(debug): print(f2.info())                                                                          
            #return like: v_s_sz000858="51~五 粮 液~000858~18.10~0.01~0.06~94583~17065~~687.07";                
            
            while True:
                f3= f2.readline()
                if f3!="" and len(f3) >20:
                    strGB=self.ToGB(f3)
                    self.ParseResultStr(strGB,type)
                else:
                    if f3 =="":
                        break;
                    else:
                        print "RESPONSE NULL"
                
        except Exception,e:
            print "GetStockStrByNum",e
            
    def ParseResultStr(self,resultstr,type):                                                                          
        stocklist = ["","","","","","","","","","","","","","","","","","",""]
        b = mysqldb()
        (conn,cursor)=   b.mysql_open("gaorencai")
        if(debug): print(resultstr)
        #print resultstr
        slist=resultstr[12:-3]
        #print slist
        if(debug): print(slist)                                                                             
        slist=slist.split('~')                                                                              
                                                                                                            
        if(debug) : print(slist)
        #print slist
        try:
            """
            #short 型
            print('*******************************')                                                           
            print u' 股票名称:', slist[1]                                                                     
            print u'  股票代码:', slist[2]                                                                     
                                                                                                                
            print u'  当前价格:', slist[3]                                                                      
            print u'  涨    跌:', slist[4]                                                                      
            print u'  涨   跌%:', slist[5],'%'                                                                  
            print u'成交量(手):', slist[6]                                                
            print u'成交额(万):', slist[7]
            """
            """
            print u'时     间:', slist[30]
            print u' 股票名称:', slist[1]
            print u' 股票代码:', slist[2]                                                                                                                                                                                
            print u' 当前价格:', slist[3]                                                                      
            print u' 昨日收盘:', slist[4]                                                                      
            print u' 今日开盘',  slist[5]                                                                 
            print u'成交量(手):', slist[6]                                                
            print u'涨跌幅   :', slist[31]
            print u'涨跌率   :', slist[32]
            print u'最高价   :', slist[33]
            print u'最低价   :', slist[34]
            print u'成交量(万):', slist[37]
            print u'换手率    :', slist[38]
            print u'市盈率    :', slist[39]
            print u'市静率     :', slist[43]
            print u'流通市值   :', slist[44]
            print u'总市值     :', slist[45]
            """
            stocklist[0] = slist[30]
            stocklist[1] = slist[2]
            stocklist[2] = slist[3]
            stocklist[3] = slist[4]
            stocklist[4] = slist[5]
            stocklist[5] = slist[6]
            stocklist[6] = slist[31]
            stocklist[7] = slist[32]
            stocklist[8] = slist[33]
            stocklist[9] = slist[34]
            stocklist[10] = slist[37]
            stocklist[11] = slist[38]
            stocklist[12] = slist[39]
            stocklist[13] = slist[43]
            stocklist[14] = slist[44]
            stocklist[15] = slist[45]
            
            #print stocklist
            print "insert into stocktable "+ slist[2]
            #b.mysql_insert(conn,cursor,stocklist,"stocktest")
            #print "type = ",type
            if type ==CHECK_MONEYFLOW_ALL_TYPE:
                b.mysql_insert(conn,cursor,stocklist,"stocktable")
            else:
                if type == CHECK_MONEYFLOW_SMALL_TYPE:
                    b.mysql_insert(conn,cursor,stocklist,"stocktabletimely")
            b.mysql_colse(conn,cursor)
        except Exception,e:
            print "ParseResultStr",e
            
            
    def GetStockInfo(self,num,type):
        #print num
        str= self.GetStockStrByNum(num,type)                                                                 
        #strGB=self.ToGB(str)                                                                             
        #self.ParseResultStr(strGB.strip())
        
    def ToGB(self,str):                                                                                          
        if(debug): print(str)                                                                               
        return str.decode('gb2312','ignore')


from datetime import datetime,date
import time
class StockMoneyFlow:                                                                                            
                                                                                        
                                                                                                            
    def GetStockMoneyFlow(self,num,type):                                                                              
        try:
            f1= urllib2.Request('http://qt.gtimg.cn/q=ff_'+ str(num))
            f2=urllib2.urlopen(f1)
            #print f2
            print(f2.geturl()) 
            if(debug): print(f2.geturl())                                                                        
            if(debug): print(f2.info())                                                                                    
            f3= f2.readline()
            #print f3 + "len(f3)" + len(f3)
            if f3!="" and len(f3) >20:
                strGB=self.ToGB(f3)
                #print "gaorencai****" + strGB
                self.ParseResultStr(strGB,type)
            else:
                print "f2.geturl() reponse NULL"
                print num
                
        except Exception,e:
            print "GetStockMoneyFlow",e
            
    def ParseResultStr(self,resultstr,type):                                                                          
        stocklist = ["","","","","","","","","","",""]
        b = mysqldb()
        (conn,cursor)=   b.mysql_open("gaorencai")
        if(debug): print(resultstr)
        #print resultstr
        slist=resultstr[17:-3]
        #print "gaorencai1" + slist
        if(debug): print(slist)                                                                             
        slist=slist.split('~')                                                                              
                                                                                                            
        if(debug) : print(slist)
        #print slist
        try:
            if type ==CHECK_MONEYFLOW_ALL_TYPE:
                stocklist[0] = slist[13]
            else:
                now = datetime.now()
                t1 = str(now).split('.')
                stocklist[0] = t1[0]
            stocklist[1] = slist[0]
            stocklist[2] = slist[1]
            stocklist[3] = slist[2]
            stocklist[4] = slist[3]
            stocklist[5] = slist[4]
            stocklist[6] = slist[5]
            stocklist[7] = slist[6]
            stocklist[8] = slist[7]
            stocklist[9] = slist[8]
            stocklist[10] = slist[9]

            #print stocklist
            if type ==CHECK_MONEYFLOW_ALL_TYPE: # 全表更新 
                b.mysql_insert(conn,cursor,stocklist,"stockmoneyflow")
            else:
                if type ==CHECK_MONEYFLOW_SMALL_TYPE: # 部分更新更新
                    b.mysql_insert(conn,cursor,stocklist,"stockmoneyflowtimely")
                else:
                    print "type erro",type
            b.mysql_colse(conn,cursor)
        except Exception,e:
            print "ParseResultStr",e
            
            
    def GetStockInfo(self,num):
        #print num
        str= self.GetStockStrByNum(num)                                                                 
        #strGB=self.ToGB(str)                                                                             
        #self.ParseResultStr(strGB.strip())
        
    def ToGB(self,str):                                                                                          
        if(debug): print(str)                                                                               
        return str.decode('gb2312','ignore')

"""
数据库
"""

import MySQLdb
import xlrd
import datetime

class mysqldb:


    def createtablenew(self):
        (conn,cursor)=   self.mysql_open("gaorencai")
        cursor.execute("use stock")
        
        f = open("D:\BaiduYunDownload\createtable.txt", "r")
        lineall =[""]

        while True:
            line = f.readline().strip('\r\n').strip('\\').strip(' ')
            if line:    
                if line[1:-1]=='END':   # The End of the file
                    break
                else:
                    if line[0]=='#':
                        line = f.readline().strip('\r\n').strip('\\').strip(' ')
                        while line[-1]!=';':
                            lineall.append(line)
                            line = f.readline().strip('\r\n').strip('\\').strip(' ')
                    
                        lineall.append(line)
                        linenew= ''.join(lineall)
                        if debug==True:print linenew
                        try:
                            cursor.execute(linenew)
                        except Exception,e:
                            print "gaorencai ",e
                        lineall=[""]

         
        self.mysql_colse(conn,cursor)
        f.close()

        
    def mysql_open(self,tablename):
        """
        connection=MySQLdb.connect(host='127.0.0.1',
                    user='omar',
                    port = 3306,
                    passwd='1234567',
                    db='stock',charset='utf-8')
        """
        connection=MySQLdb.connect(host='127.0.0.1',
                    user='omar',
                    port = 3306,
                    passwd='1234567',
                    db='stock')
        
        cursor = connection.cursor()   
        return connection,cursor

    def mysql_opench(self,tablename):
        """
        connection=MySQLdb.connect(host='127.0.0.1',
                    user='omar',
                    port = 3306,
                    passwd='1234567',
                    db='stock',charset='utf-8')
        """
        connection=MySQLdb.connect(host='127.0.0.1',
                    user='omar',
                    port = 3306,
                    passwd='1234567',
                    db='stockch',
                    charset='utf8')
        
        cursor = connection.cursor()   
        return connection,cursor
    def mysql_insert(self,connection,cursor,strlist,tablename):
        try:
            if tablename=="stocktabletimely":
                date_float = strlist[0]
                #date = datetime.date.fromordinal(datetime.date(1899,12,31).toordinal()-1 + int(date_float))
                date = strlist[0]
                stockcode = strlist[1]
                current_price   = strlist[2]
                yesterday_price  = float(strlist[3])
                open_price  = strlist[4]
                turnover_vol  = strlist[5]
                updown_scal  = strlist[6]
                updown_ration  =strlist[7]
                highest_price  = strlist[8]
                lowest_price  = strlist[9]
                turnover_total  = strlist[10]
                turnover_ration  = strlist[11]
                price_earning_ration  = strlist[12]
                price_to_book_ratio   = strlist[13]
                Circulation_market_value  =strlist[14]
                total_market_value = strlist[15]
                insertsql = "insert into stocktabletimely(datetime,stockcode,current_price,yesterday_price,open_price,\
                             turnover_vol,updown_scal,updown_ration,highest_price,lowest_price,\
                             turnover_total,turnover_ration,price_earning_ration,price_to_book_ratio,Circulation_market_value,\
                             total_market_value) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update current_price =%s,\
                             yesterday_price=%s,open_price=%s, turnover_vol=%s,updown_scal=%s,updown_ration=%s,highest_price=%s,lowest_price=%s,\
                             turnover_total=%s,turnover_ration=%s,price_earning_ration=%s,price_to_book_ratio=%s,Circulation_market_value=%s,total_market_value=%s"
                cursor.execute(insertsql,(date,stockcode,current_price,yesterday_price,open_price,turnover_vol,updown_scal,updown_ration,highest_price,lowest_price,turnover_total,turnover_ration,price_earning_ration,price_to_book_ratio,Circulation_market_value,total_market_value,current_price,yesterday_price,open_price,turnover_vol,updown_scal,updown_ration,highest_price,lowest_price,turnover_total,turnover_ration,price_earning_ration,price_to_book_ratio,Circulation_market_value,total_market_value))

            else :
                if tablename=="stockmoneyflow":
                   
                    insertsql = "insert into stockmoneyflow(date,stockcode,master_in,master_out,master_net,\
                                 master_in_total_ration,small_in,small_out,small_net,small_in_out_ration,\
                                 totalmoney) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update master_in = %s,\
                                 master_out=%s,master_net=%s,master_in_total_ration=%s,small_in=%s,small_out=%s,small_net=%s,small_in_out_ration=%s,totalmoney=%s"
                                
                    cursor.execute(insertsql,(strlist[0],strlist[1],strlist[2],strlist[3],strlist[4],strlist[5],strlist[6],strlist[7],strlist[8],strlist[9],strlist[10],strlist[2],strlist[3],strlist[4],strlist[5],strlist[6],strlist[7],strlist[8],strlist[9],strlist[10]))
                    
                    #cursor.execute(insertsql,(date,stockcode,current_price,yesterday_price,open_price,turnover_vol,updown_scal,updown_ration,highest_price,lowest_price,turnover_total,turnover_ration,price_earning_ration,price_to_book_ratio,Circulation_market_value,total_market_value))

                else:
                    if tablename=="stocktable":
                        date_float = strlist[0]
                        #date = datetime.date.fromordinal(datetime.date(1899,12,31).toordinal()-1 + int(date_float))
                        date = strlist[0]
                        stockcode = strlist[1]
                        current_price   = strlist[2]
                        yesterday_price  = float(strlist[3])
                        open_price  = strlist[4]
                        turnover_vol  = strlist[5]
                        updown_scal  = strlist[6]
                        updown_ration  =strlist[7]
                        highest_price  = strlist[8]
                        lowest_price  = strlist[9]
                        turnover_total  = strlist[10]
                        turnover_ration  = strlist[11]
                        price_earning_ration  = strlist[12]
                        price_to_book_ratio   = strlist[13]
                        Circulation_market_value  =strlist[14]
                        total_market_value = strlist[15]
                        insertsql = "insert into stocktable(date,stockcode,current_price,yesterday_price,open_price,\
                                     turnover_vol,updown_scal,updown_ration,highest_price,lowest_price,\
                                     turnover_total,turnover_ration,price_earning_ration,price_to_book_ratio,Circulation_market_value,\
                                     total_market_value) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update current_price =%s,\
                                     yesterday_price=%s,open_price=%s, turnover_vol=%s,updown_scal=%s,updown_ration=%s,highest_price=%s,lowest_price=%s,\
                                     turnover_total=%s,turnover_ration=%s,price_earning_ration=%s,price_to_book_ratio=%s,Circulation_market_value=%s,total_market_value=%s"
                        cursor.execute(insertsql,(date,stockcode,current_price,yesterday_price,open_price,turnover_vol,updown_scal,updown_ration,highest_price,lowest_price,turnover_total,turnover_ration,price_earning_ration,price_to_book_ratio,Circulation_market_value,total_market_value,current_price,yesterday_price,open_price,turnover_vol,updown_scal,updown_ration,highest_price,lowest_price,turnover_total,turnover_ration,price_earning_ration,price_to_book_ratio,Circulation_market_value,total_market_value))

                    else:
                        if tablename=="blockmoneyflow":
                            date  = strlist[0]
                            blockname  = strlist[1]
                            level   = strlist[2]
                            statics  =strlist[3]
                           
                            insertsql = "insert into blockmoneyflow(date,blockname,level,statics) values(%s,%s,%s,%s) on duplicate key update statics =%s"
                            #print insertsql
                            cursor.execute(insertsql,(date,blockname,level,statics,statics))

                            
                        else:
                            if tablename=="stockcodeblock":
                                stockcode  = strlist[0]
                                blockname  = strlist[1]
                                insertsql = "insert into stockcodeblock(stockcode,blockname) values(%s,%s)"
                                #print insertsql
                                cursor.execute(insertsql,(stockcode,blockname))

                            else:
                                if tablename =="stockpricelevel":
                                    blockname     = strlist[0]
                                    stockcode     = strlist[1]
                                    date          = strlist[2]
                                    updown_ration = strlist[3]

                                    insertsql = "insert into stockpricelevel(blockname,stockcode,date,updown_ration) values(%s,%s,%s,%s)"
                                    cursor.execute(insertsql,(blockname,stockcode,date,updown_ration))

                                else:

                                    if tablename=="stockmoneyflowtimely":
                                        print "gaorencai "
                                        insertsql = "insert into stockmoneyflowtimely(datetime,stockcode,master_in,master_out,master_net,\
                                                     master_in_total_ration,small_in,small_out,small_net,small_in_out_ration,\
                                                     totalmoney) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update master_in = %s,\
                                                     master_out=%s,master_net=%s,master_in_total_ration=%s,small_in=%s,small_out=%s,small_net=%s,small_in_out_ration=%s,totalmoney=%s"

                                        cursor.execute(insertsql,(strlist[0],strlist[1],strlist[2],strlist[3],strlist[4],strlist[5],strlist[6],strlist[7],strlist[8],strlist[9],strlist[10],strlist[2],strlist[3],strlist[4],strlist[5],strlist[6],strlist[7],strlist[8],strlist[9],strlist[10]))

                                    else:
                                        print "table name  error"
                
        except Exception,e:
            print "mysql_insert",e

    def cleartable(self,connection,cursor,tablename):
        sql="delete from "+tablename
        try:
            cursor.execute(sql)
        except Exception, e:
            print "clear table failed" + tablename
    def mysql_select(self,connection,cursor,strlist,tablename):
        if tablename == "stockmoneyflow":
            try:
                #print strlist
                strdate = "2015-12-29"#strlist[0]
                master_in_total_ration = 10
                sql ="select stockcode,master_in,master_out,master_net from stockmoneyflow where date = %s and master_in_total_ration > %s"
                #sql ="select * from stockmoneyflow where date = %s and master_in_total_ration > %s"
                #cursor.execute(sql,[strdate,master_in_total_ration])
                cursor.execute(sql,[strlist[0],strlist[1]])
                return cursor.fetchall()
            except Exception,e:
                print "stockmoneyflow exception "
                print e
        else:
            if tablename =="stocktest":
                try:
                    sql ="select * from stocktest where date = %s and stockcode = %s"
                    cursor.execute(sql,[strlist[0],strlist[1]])
                    return cursor.fetchall()
                except Exception,e:
                    print e
            else:
                print tablename
        
    def mysql_colse(self,connection,cursor):
        connection.commit()
        #cursor = connection.cursor()
        cursor.close
        connection.close

        
    def mysql_select_adapt(self,connection,cursor,sqlstr):

        try:
            cursor.execute(sqlstr)
            return cursor.fetchall()
        except Exception,e:
            print "mysql_select_adapt",e

import smtplib                                                                           
from email.mime.text import MIMEText                                                     
from email.header import Header   
class Email:
    
    def Email_send(self,receiver_address,subject,contex):
        sender = '18565884653@163.com'
        if receiver_address!="":
            #receiver = "328469211@qq.com"
            receiver = receiver_address
        else:
            receiver = "328469211@qq.com"
        subject = subject + '股市风险 测试'                                                         
        smtpserver = 'smtp.163.com'                                                              
        username = '18565884653'                                                                         
        password = 'ovybamldshocgybw'                                                                         
        #password = 'Gao19830220'                                                                                          
        msg = MIMEText('新年课程表\n'+contex,'plain','utf-8')           
        msg['Subject'] = Header(subject, 'utf-8')                                                
        msg['From'] = '18565884653<18565884653@163.com>'    
        msg['To'] = "328469211@qq.com"
        try:                                                                                  
            smtp = smtplib.SMTP()                                                                    
            smtp.connect('smtp.163.com')                                                             
            smtp.login(username, password)                                                           
            smtp.sendmail(sender, receiver, msg.as_string())                                         
            smtp.quit()
            print "邮件发送成功"
        except Exception,e:
            print "邮件发送失败"
            print e



class GETSTOCK:

    def __init__(self):
        self.a=StockInfo()
        self.b=mysqldb()
    
    def getstockandsave(self):
        #self.b.createtable("stocktable")
        #self.b.createtable("stocktest")
        temp =["","",""]
        self.f = open("D:\BaiduYunDownload\stockinfo.txt", "r")
        start =time.clock()
        count = 0
        linenewall=[""]
        linetotal =""
        while True:
            #print "count " + str(count)
            line = self.f.readline().strip('\r\n')
            #print line 
            if line:
                #try:
                number =string.atoi(line)
                if number < 600000:
                    linenew ='sz'+line
                else:
                    linenew = 'sh'+line
                    
                if count < MAXSTOCKNAM:
                    
                    if count == 0:
                        print "count " + str(count)
                        linenewall[0]=linenew
                        count=count+1
                    else:
                        print "count " + str(count)
                        linenewall.append(linenew)
                        count=count+1
                else:
                    count =0
                    linenewall.append(linenew)
                    print linenewall
                    self.a.GetStockInfo(','.join(linenewall),CHECK_MONEYFLOW_ALL_TYPE)
                    linenewall=[""]
                   
            else:
                print "gaorencai"
                if count == 0:
                    break
                else:
                    count =0
                    print linenewall
                    self.a.GetStockInfo(','.join(linenewall),CHECK_MONEYFLOW_ALL_TYPE)
                    linenewall=[""]
        self.f.close()
        end =time.clock()
        print "time diff = %f s " % (end - start) 
            #email1 = Email()
            #email1.Email_send("omar.gao@nokia.com","今天下午  王总要来参加会议  大家注意了","time_diff =%f s" %(end-start))
        
class GETSTOCK_Small:
    def __init__(self):
        self.a=StockInfo()
    def getstockandsave(self):
        count = 0
        linenewall=[""]
        self.f = open("D:\BaiduYunDownload\position.txt", "r")
        start =time.clock()
        while True:
            line = self.f.readline().strip('\n')
            if line:
                if line[0]!='#':
                    number =string.atoi(line[0:6])
                    print line[0]
                    print 'code = ',line[0:6]
                    if number < 600000:
                        linenew ='sz'+line[0:6]
                    else:
                        linenew = 'sh'+line[0:6]
                    print linenew
                    if count < MAXSTOCKNAM:
                    
                        if count == 0:
                            print "count " + str(count)
                            linenewall[0]=linenew
                            count=count+1
                        else:
                            print "count " + str(count)
                            linenewall.append(linenew)
                            count=count+1
                    else:
                        count =0
                        linenewall.append(linenew)
                        print linenewall
                        print 'set',list(set(linenewall))
                        linenewall=[""]
                        #self.a.GetStockMoneyFlow(linenew,CHECK_MONEYFLOW_SMALL_TYPE)
                        self.a.GetStockInfo(','.join(list(set(linenewall))),CHECK_MONEYFLOW_SMALL_TYPE)
            else:
                if count == 0:
                    break
                else:
                    count =0
                    print linenewall
                    print 'set',list(set(linenewall))
                    self.a.GetStockInfo(','.join(list(set(linenewall))),CHECK_MONEYFLOW_SMALL_TYPE)
                    linenewall=[""]
        self.f.close()
        end =time.clock()
        print "time diff = %f s " % (end - start)
    
class GETMoneyFlow:
    def __init__(self):
        
        self.a=StockMoneyFlow()
        self.b=mysqldb()
    def getstockandsave(self):
        print "gaorencai0 "
        #self.b.createtable("stockmoneyflow")
        print "gaorencai 1"
        self.f = open("D:\BaiduYunDownload\stockinfo.txt", "r")
        start =time.clock()
         
        while True:
            line = self.f.readline().strip('\n')
            if line:
                number =string.atoi(line)
                if number < 600000:
                    linenew ='sz'+line
                else:
                    linenew = 'sh'+line
                self.a.GetStockMoneyFlow(linenew,CHECK_MONEYFLOW_ALL_TYPE)
            else:
                break
        self.f.close()
        end =time.clock()
        print "time diff = %f s " % (end - start)

    def selectdata(self):
        (conn,cursor)=   self.b.mysql_open("gaorencai")
        strlist=["",0]
        strlist[0]="2015-12-29"
        strlist[1]=10
        return self.b.mysql_select(conn,cursor,strlist,"stockmoneyflow")
    
    def selectdata_adapt(self,strsql):
        (conn,cursor)=   self.b.mysql_open("gaorencai")
        #strlist=["",0]
        #strlist[0]="2015-12-29"
        #strlist[1]=10
        ration = 10
        strsql = "select * from stockmoneyflow where master_in_total_ration >" + str(ration) +" and date = '2016-01-08'"
        #print strsql
        return self.b.mysql_select_adapt(conn,cursor,strsql)

class GETMoneyFlow_Small:
    def __init__(self):
        self.a=StockMoneyFlow()
        
    def getstockandsave(self):

        self.f = open("D:\BaiduYunDownload\position.txt", "r")
        start =time.clock()
        listset = [""]
        linenew=""
        while True:
            line = self.f.readline().strip('\n')
            if line:
                if line[0]!='#':
                    number =string.atoi(line[0:6])
                    print line[0:6]
                    if number < 600000:
                        linenew ='sz'+line[0:6]
                    else:
                        linenew = 'sh'+line[0:6]
                    print linenew
                    listset.append(linenew)
                    
            else:
                break
        for x in list(set(listset)):
            self.a.GetStockMoneyFlow(x,CHECK_MONEYFLOW_SMALL_TYPE)
            
        self.f.close()
        end =time.clock()
        print "time diff = %f s " % (end - start)

    def checking(self):
        print " " 

#-*- coding:utf-8 -*-s = u’示例’ 
##获取板块信息
import urllib2
import codecs 
import sys
import string
class Getblock:
    
    def __init__(self):
        
        self.b=mysqldb()
        
    def getstockblock(self):
        print sys.getdefaultencoding()
        self.f = open(r"D:\BaiduYunDownload\stockinfo.txt", "r")
        #self.fileout = open(r'D:\BaiduYunDownload\blockinfo.txt', 'wb')
        self.fileout = codecs.open('blockinfo.txt', 'w','utf-8')
        while True:
            line = self.f.readline().strip('\n')
            if line:
                number =string.atoi(line)
                if number < 600000:
                    linenew ='sz'+line
                else:
                    linenew = 'sh'+line
                print linenew
                self.GetBlockInfo(linenew,self.fileout)
            else:
                break
        self.f.close()
        self.fileout.close()
    def GetBlockInfo(self,stockcode,fileout):
        f1= urllib2.Request('http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code=' + str(stockcode))
        #f1= urllib2.Request('http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code=sz000016')
        try:

            f2=urllib2.urlopen(f1)
            if(debug): print(f2.geturl())                                                                        
            if(debug): print(f2.info())
            str1 =""
            while True:
                stockinfo = f2.readline()
                if stockinfo:
                    if 'summary' in stockinfo:
                        stockinfoencode = stockinfo.decode('utf8','ignore')
                        #print stockinfoencode
                        stockinfosplit =stockinfoencode.split('<')
                        stocknamelist = stockinfosplit[4].split('>')
                        #print stocknamelist[1]
                        str1 = stocknamelist[1].strip()
                        #print str1
                        stocknamelist1= str1.split('。'.decode('utf-8'))
                        #print stocknamelist1[0]
                        stocknamelist2 = stocknamelist1[0].split('，'.decode('utf-8'))
                        
                        print stocknamelist2[0]
     
                        if len(stocknamelist2) > 0:
                            fileout.write(stockcode+',')
                            gao = ','.join(stocknamelist2)
                            print gao
                            #gao = '\r\n'.join(stocknamelist2)
                            fileout.write(gao+'\r\n')
                         
                        #reload(sys)  
                        #sys.setdefaultencoding('ascii')
                        
                else:
                    break
        except Exception,e:
                print e
    def insertDb(self):
        (conn,cursor)=   self.b.mysql_opench("gaorencai")
        self.b.cleartable(conn,cursor,"stockcodeblock")
        try:
            self.filein = codecs.open('blockinfo.txt', 'r','utf-8')
            number = 0
            blockname=[]
            stockcode=[]
            stockall=[]
            strsqllist=['','']
            while True:
                line = self.filein.readline().strip('\r\n')
                #line = self.filein.readline().strip(' ')
                if line:
                    linetemp =line.split(',')
                    lenx= len(linetemp)
                    print lenx
                    number = 1
                    strsqllist=['','']
                    while True:
                        if number <lenx:
                            print linetemp[0]
                            print number
                            strtemp =''.join(linetemp[0])
                            print strtemp[2:]
                            strsqllist[0]=str(strtemp[2:])
                            #print "gao" & strsqllist[0]
                            strsqllist[1]=linetemp[number].encode('utf-8')
                            self.b.mysql_insert(conn,cursor,strsqllist,"stockcodeblock")
                            number=number + 1
                            #print datastrsql
                        else:
                            break
                else:
                    break
            self.filein.close()

        except Exception,e:
            print e

        self.b.mysql_colse(conn,cursor)
        print "done....."



    def MakeAnalysis(self,date):
        PRICELEVEL =[9,8,7,6,5,4,3,2,1] #价格涨幅
        MONEYFLOWLEVEL=[30,25,20,15,10,5,1] # 资金流量 主力百分比
        #self.b.createtable("blockmoneyflow")
        try:
            self.filein = codecs.open('blockinfo.txt', 'r','utf-8')
            number = 0
            blockname=[]
            stockcode=[]
            stockall=[]
           
            while True:
                line = self.filein.readline().strip('\r\n')
                #line = self.filein.readline().strip(' ')
                if line:
                    
                    linetemp =line.split(',')
                    stockall.append(linetemp)
                    stockcode.append(linetemp[0])
                    #print linetemp[0]
                    blockname.extend(linetemp[1:])
                    number =number +1
                    
                else:
                    break
            blockname=list(set(blockname))
            print len(blockname)

            """
            for x in blockname:
                print x
            
            for x in stockcode:
                print x
            """
            self.filein.close()
            for x in PRICELEVEL:
                self.MakeAnalysisPriceLevel(stockall,blockname,stockcode,x,date)      #上涨幅度
            for x in MONEYFLOWLEVEL:
                self.MakeAnalysisMoneyFlowLevel(stockall,blockname,stockcode,x,date) # 资金流量等级
            
        except Exception,e:
            print e
        
        print "done....."
        
     
        
    def MakeAnalysisPriceLevel(self,pricelevel):

        (conn,cursor)=   self.b.mysql_opench("gaorencai")

        self.b.cleartable(conn,cursor,"stockpricelevel")

        strsql = "select distinct blockname from stockcodeblock"
        strsql2 =""
        result= self.b.mysql_select_adapt(conn,cursor,strsql)

        #print result
        
        for x in result:
            print x[0]
            strsql1 = "select stockcode from stockcodeblock where blockname ='" + x[0]+"'"
            print strsql1
            resultstockcode = self.b.mysql_select_adapt(conn,cursor,strsql1)
            for y in resultstockcode:
                strsql2= "select date,updown_ration from stock.stocktable where updown_ration > " + str(pricelevel) +" and  stockcode =" + y[0]
                print strsql2
                resultshare = self.b.mysql_select_adapt(conn,cursor,strsql2)
                strsqllist=['','','','']
                
                if resultshare :
                    print resultshare
                    #print resultshare[0]
                    #print resultshare[0][0]
                    strsqllist[0]=x[0] # 板块
                    strsqllist[1]=y[0] # 股票代码
                    strsqllist[2]=resultshare[0][0]  # 日期
                    strsqllist[3]=resultshare[0][1] # 涨跌幅
                    #strsqllist[3]=9 # 涨跌幅
                    self.b.mysql_insert(conn,cursor,strsqllist,"stockpricelevel")
                    
                
        self.b.mysql_colse(conn,cursor)
    def MakeAnalysisMoneyFlowLevel(self,stockall,blockname,stockcode,moneyflowlevel,date):
        (conn,cursor)=   self.b.mysql_opench("gaorencai")
        #print len(blockname)
        stockstatics = [0]*len(blockname)
        strlist=["",0]
        datastrsql =["","",0,0]
        strlist[0]=date
        strlist[1]=moneyflowlevel
        strsql = "select stockcode,master_in,master_out,master_net from stock.stockmoneyflow where date = '" + str(date) + "' and master_in_total_ration > " + str(moneyflowlevel)
        #print strsql
        result= self.b.mysql_select_adapt(conn,cursor,strsql)
        #print result
        for x in result:
            #print "gao",x
            number =string.atoi(x[0])
            #print x[0]
            if number < 600000:
                linenew ='sz'+x[0]
            else:
                linenew = 'sh'+x[0]
            for y in stockall:
                if linenew==y[0]:  #找到对应股票代码的板块信息
                    #print x[0]
                    #print y[0]
                    for z in y[1:]:
                        try:
                            index =blockname.index(z)
                            stockstatics[index]=stockstatics[index]+1
                        except Exception,e:
                            print e
                    #print len(y)-1
                    

        #print stockstatics
        #print len(stockstatics)
        
        for x in blockname:
            #print x
            
            datastrsql[0]=date
            datastrsql[1]=x.encode('utf-8')
            datastrsql[2]=moneyflowlevel
            #blocknameinex  = blockname.index(x)
            #print blocknameinex
            datastrsql[3]= stockstatics[blockname.index(x)]
            #print datastrsql
            #print datastrsql
            self.b.mysql_insert(conn,cursor,datastrsql,"blockmoneyflow")
            

        self.b.mysql_colse(conn,cursor)
            
        """
        print len(stockall)
        for x in stockall:
            print "x= ",len(x)
        """
        #print moneyflowlevel


        
##################################################################################
from datetime import datetime,date
debug=False

class datetimetransform:
    
    def __init__(self):
        #2016 节假日 安排 
        self.holidaydate=[]
        self.holidaysstr = [
             [2016, 1, 1],
             [2016, 1, 2],
             [2016, 1, 3],
             [2016, 2, 7],
             [2016, 2, 8],
             [2016, 2, 9],
             [2016, 1, 10],
             [2016, 2, 11],
             [2016, 2, 12],
             [2016, 2, 13],
             [2016, 4, 2],
             [2016, 4, 3],
             [2016, 4, 4],
             [2016, 5, 1],
             [2016, 5, 2],
             [2016, 6, 9],
             [2016, 6, 10],
             [2016, 6, 11],
             [2016, 9, 15],
             [2016, 9, 16],
             [2016, 9, 17],
             [2016, 10, 1],
             [2016, 10, 2],
             [2016, 10, 3],
             [2016, 10, 4],
             [2016, 10, 6],
             [2016, 10, 7]]
        
        self.exceptholidaydate=[]
        self.exceptholidaysstr= [
             [2016, 2, 6],
             [2016, 2, 14],
             [2016, 6, 12],
             [2016, 9, 18],
             [2016, 10, 8],
             [2016, 10, 9]]
        # 周一  至周五  是工作日 
        self.weekday=[0,1,2,3,4]

        
        
    def transferdateformat(self,originaldatestr,newdateformat):
        datelist=[]
        for x in originaldatestr:
            #print x
            datetimetemp= ''.join(str(x)).strip('[]').replace(',','-').replace(' ','')
            datelist= datetimetemp.split('-')
            for y in datelist[1:]:
                if len(y)<2:
                    y1='0'+str(y)
                    #print y
                    datelist[datelist.index(y)]=y1

            if debug ==True: print 'transferdateformat', datelist
            #newdateformat.append(datetime.strptime(datetimetemp,'%Y-%m-%d'))
            #datetimeformattemp =datetime.strptime(datetimetemp,'%Y-%m-%d')
            #print datetimeformattemp
            #newdateformat.append(datetime.strptime(datetimetemp,'%Y-%m-%d'))
            newdateformat.append(datelist)

    def checkinginterset(self):
        #listtemp= list(set(self.holidaysstr).intersection(set(self.exceptholidaysstr)))
        if debug ==True: print self.holidaydate
        if debug ==True: print self.exceptholidaydate
        for x in self.holidaydate:
            if x in self.exceptholidaydate:
                return True
                                                 
    def isworkday(self):
        
        weekday = datetime.now().weekday()
        
        if weekday in  self.weekday:
            if debug ==True:print 'isworkday',weekday
            print 'isworkday',weekday
            return True
        else:
            if debug ==True:print 'isworkday',weekday
            return False
    def isholiday(self):
        
        datetimetemp = date.today()
        datetimetemplist =  str(datetimetemp).split('-')
        if debug ==True:print 'isholiday:',datetimetemplist
        if debug ==True:print 'isholiday:',self.holidaydate
        if datetimetemplist in  self.holidaydate:
            if debug ==True:print datetimetemplist,"isholiday-- holiday"
            return True
        else:
            if debug ==True:print datetimetemplist,"isholiday-- workingday"
            return False
        
    def isexceptholiday(self):
        
        datetimetemp = date.today()
        datetimetemplist =  str(datetimetemp).split('-')
        if debug ==True:print 'isexceptholiday',datetimetemplist
        if datetimetemplist in  self.exceptholidaydate:
            
            if debug ==True: print datetimetemplist,"isexceptholiday ---exceptholiday"
            return True
        else:
            if debug ==True:  print datetimetemplist,"isexceptholiday  today doesn't exceptholiday "
            return False
        
    def dateprint(self,output):
        print output
        #print self.exceptholidaydate

        
from datetime import datetime,date
import time
class WorkingTime:
    
    def __init__(self):
        self.working_start_time = '09:30.00'
        self.working_stop_time =  '15:00.00'
        self.sleepseconds = 0
        
    def isworktime(self):
        now = datetime.now()
        time_temp= str(now).split(' ')
        start_time_str =time_temp[0] +  ' ' + self.working_start_time
        stop_time_str = time_temp[0] +  ' ' + self.working_stop_time
        

        t1 = time.strptime(start_time_str,"%Y-%m-%d %H:%M.%S")
        t2 = time.strptime(stop_time_str,"%Y-%m-%d %H:%M.%S")

        t1=datetime(t1[0],t1[1],t1[2],t1[3],t1[4],t1[5])
        t2=datetime(t2[0],t2[1],t2[2],t2[3],t2[4],t2[5])
        if debug ==True: 
            print (t1-t2).days
            print (t2-t1).days
            print (t1-t2).seconds
            print (t2-t1).seconds
            print (now -t1).days
            print (now -t2).days
            print (t1 -now).seconds
            print (now -t2).seconds
        
        if (now -t1).days ==0 and (t2-now).days ==0:
            if debug ==True: print "True"
            return True
        else:
            if debug ==True: print "False"
            self.sleepsecond = (t1 -now).seconds
            return False
        
    def getsleeptime(self):
        if debug ==True: print "get the sleepseconds = ",self.sleepsecond
        return self.sleepsecond

    
class Check_Holiday_Working_Time:
        
    def checkholidayandworkingtime(self):
        isworkingdayflag = False
        isworkingtimeflag = False
        sleeptimeneed=0
        dtt= datetimetransform()
        dtt.transferdateformat(dtt.holidaysstr,dtt.holidaydate)
        if debug ==True:dtt.dateprint(dtt.holidaydate)
        dtt.transferdateformat(dtt.exceptholidaysstr,dtt.exceptholidaydate)
        if debug ==True:dtt.dateprint(dtt.exceptholidaydate)
        if dtt.checkinginterset()==True:
            print "WARNING: duplicate tuple in holidaydate and exceptholidaydate"
        else:
           
            if dtt.isworkday() ==True:
                if dtt.isholiday():
                    if debug ==True:print "Today no need working0"
                else:
                    isworkingdayflag =True
                    if debug ==True:print "Today is working day0"
                    

            else:
                if dtt.isexceptholiday():
                    isworkingdayflag=True
                    if debug ==True:print "Today is working day"

                else:
                    if debug ==True:print "Today no need work"
        if isworkingdayflag ==True:
            wt =WorkingTime()
            isworkingtimeflag= wt.isworktime()
            if isworkingtimeflag ==True:
                sleeptimeneed =10
                if debug ==True:print "is working "
            else:
                sleeptimeneed = wt.getsleeptime()
                if debug ==True:print "The process will sleep seconds = ",sleeptimeneed
        else:
            isworkingdayflag=False
            isworkingtimeflag=False
            sleeptimeneed = 32400 # 9个小时
            #sleeptimeneed = 10
            
        return isworkingdayflag,isworkingtimeflag,sleeptimeneed






import string
MAX_USER = 3  # 最大用户数
MAX_TUPLE_ONUSER =5

class warningcheck:
    
    def __init__(self):
        self.b=mysqldb()
        self.f = open("D:\BaiduYunDownload\position.txt", "r")
        self.emailaddress = []
        self.position = [[]*MAX_TUPLE_ONUSER for rows in range(MAX_USER)]
        self.emailaddressprice =[]
        self.email1 = Email()
        count=0
        while True:
            line = self.f.readline().strip('\r\n').strip(' ')
            if line :
                if line[1:-1]=='END':
                    break
                else:
                    if line[0]=='#':
                        self.emailaddress.append(line[1:-1])
                    else:
                        self.position[count].append(line.strip(';').split('#'))
                        #position[count].append(line)
                        #print "count = ",count
                        if line[-1]==';':
                            count=count+1
                            if count>MAX_USER:
                                print "WRNNING overflow count> MAX_USER ",count,MAX_USER
                                break;
        #print len(self.position)
        #print len(self.position[0])
        #print self.emailaddress

        #for x in self.position:
        #    print x

        self.f.close()

    def checkprice(self):  # 止损位
        (conn,cursor)=   self.b.mysql_open("gaorencai")
        result = []
        sqlstr=""
        warninglog=[[]*MAX_TUPLE_ONUSER for rows in range(MAX_USER)]
        emailtext =[]
        for x in self.emailaddress:
            emailaddressprice= self.position[self.emailaddress.index(x)]
            #print len(emailaddressprice)
            for y in emailaddressprice:
                print x,y
                sqlstr = "select current_price from stocktabletimely where stockcode = "+ str(y[0]) + " order by datetime desc";
                #print sqlstr
                result= self.b.mysql_select_adapt(conn,cursor,sqlstr)
                if result:
                    test1= str(result).split('(')
                    test3= test1[2].split(',')

                    #print string.atol(test3[0]) , y[1]
                    if string.atof(test3[0]) < y[1]:  # 价格破位 
                        print "WARNNING LEVEL 1"
                        warninglog[self.emailaddress.index(x)].append(str(y[0]) + ": WARNNING LEVEL 1")
                        
                    else:
                        print "Secure now "
        #print warninglog
        index = 0
        for x in self.emailaddress:
            self.sendemail(x,str(index) +"WARNNING LEVEL1 ",warninglog[self.emailaddress.index(x)])
            sleep(5)
        index = 0
        print ' '.join(emailtext)
        
        print "checkprice done"
        
    def sendemail(self,receiverlist,subject,emailtext):  # 发送邮件
         ISOTIMEFORMAT='%Y-%m-%d %X'
         print receiverlist,subject,emailtext

         self.email1.Email_send(receiverlist,''.join( time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) ))+subject ,'\n'.join(map(lambda x:''.join(str(x)),emailtext)))
        
    def checkmasterout_oneday(self): # 一天内的主力出货情况
        
        (conn,cursor)=   self.b.mysql_open("gaorencai")
        result = []
        sqlstr=""
        warninglog=[[]*MAX_TUPLE_ONUSER for rows in range(MAX_USER)]
        emailtext =[]
        for x in self.emailaddress:
            emailaddressprice= self.position[self.emailaddress.index(x)]
            #print len(emailaddressprice)
            for y in emailaddressprice:
                print x,y
                sqlstr = "select master_in_total_ration from stockmoneyflowtimely where stockcode = "+ str(y[0]) + " order by datetime desc";
                print sqlstr
                result= self.b.mysql_select_adapt(conn,cursor,sqlstr)
                if result:
                    test1= str(result).split('(')
                    test3= test1[2].split(',')
                    print test3[0]
                    #print string.atol(test3[0]) , y[1]
                    print string.atof(test3[0]) -2
                    if string.atof(test3[0]) < -2:  # 主力有出货嫌疑
                        print "WARNNING LEVEL 1"
                        warninglog[self.emailaddress.index(x)].append(str(y[0]) + ": WARNNING LEVEL 1")
                        
                    else:
                        print "Secure now "
        print warninglog
        index = 0
        for x in self.emailaddress:
            #self.sendemail(x,str(index) +"WARNNING LEVEL1 ",warninglog[self.emailaddress.index(x)])
            #sleep(5)
            print x,warninglog[self.emailaddress.index(x)]
        index = 0
        print ' '.join(emailtext)
        
        
        print "checkmasterout_oneday done"

    def checkmasterin_one_day(self): # 一天内的主力介入情况
        print ""

    def checkmasterout_Ndays(self):  # N天内主力出货情况
        
        print ""
    def checkmasterin_Ndays(self):   # N天内主力介入情况
        print ""


##################################################################################
        
import threading
from time import ctime,sleep

class CreateThreadStack:

    def __init__(self):
        self.threads = []
        self.mydb=mysqldb()
        self.wc=warningcheck()
        self.mydb.createtablenew() #创建数据表
        
        self.getstock=GETSTOCK()
        self.moneyflow =GETMoneyFlow()
        
    def GetStock(self,func):
        #getstock =GETSTOCK()
        self.getstock.getstockandsave()
        
    def GetMoneyflow(self,func):
        #moneyflow =GETMoneyFlow()
        self.moneyflow.getstockandsave()
    def Warnningcheck(self,func):
        self.wc.checkprice()
        self.wc.checkmasterout_oneday()
    def SendEmail(self):
        ration =10
        strsql = "select stockcode as '股票代码',master_net as '主力净流入' from stockmoneyflow where master_in_total_ration >" + str(ration) +" and date = '2016-01-08'"

        emailtext= self.moneyflow.selectdata_adapt(strsql)

        try:
        
            ISOTIMEFORMAT='%Y-%m-%d %X'
            print  time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )
            email1 = Email()
            #receiverlist=["328469211@qq.com","zhaoqinyu@163.com"]
            receiverlist=["328469211@qq.com"]
            #email1.Email_send("zhaoqinyu@163.com",''.join( time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )),'\n'.join(map(lambda x:''.join(str(x)),emailtext)))
            email1.Email_send(receiverlist,''.join( time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )),'\n'.join(map(lambda x:''.join(str(x)),emailtext)))
            #email1.Email_send(receiverlist,"新年课程表","新的课程表")
        except Exception,e:
            print e

    def Run(self):
        t1 = threading.Thread(target=self.GetStock,args=(u'GetStock',))
        self.threads.append(t1)
        t2 = threading.Thread(target=self.GetMoneyflow,args=(u'GetMoneyflow',))
        self.threads.append(t2)

        for t in self.threads:
            t.setDaemon(True)
            t.start()
        t.join()
        #self.SendEmail()
        print "all over done %s" %ctime()


##################################################################################        
import time
def main():
        """
        mydb=mysqldb()
        mydb.createtablenew() #创建数据表
        gmfs=GETMoneyFlow_Small()
        gmfs.getstockandsave()
        gss = GETSTOCK_Small()
        gss.getstockandsave()

        """

        #wc=warningcheck()
        #wc.checkprice()
        #wc.checkmasterout_oneday()

        

        
        #while True:
        chwt= Check_Holiday_Working_Time()
        (isWorkingdayflag,workingtimeflag,sleeptimeneed)=chwt.checkholidayandworkingtime()
        if (isWorkingdayflag==False or workingtimeflag==False) and TESTMODE ==False:
            print "No need work ,now i will sleep ***** ",sleeptimeneed," ****seconds"
            #sleep(sleeptimeneed)
            sleep(10)
        else:
            print "working now"
            cts= CreateThreadStack()
            cts.Run()
        
        
		
        """
        #汉字无法插入数据库  已经解决
        blk =Getblock()
        #blk.getstockblock()
        #blk.MakeAnalysis("2016-06-06")
        #blk.MakeAnalysisPriceLevel(8)
        blk.insertDb()
        """
if __name__ == '__main__':
    main()

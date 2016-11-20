
        mydb.createtablenew() #创建数据表
        gmfs=GETMoneyFlow_Small()D
	          #Test merge code
		    =======


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

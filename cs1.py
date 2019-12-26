#read from daily files and insert in landing zone table
import sys
import psycop2
#connection to database
conn=psycop2.connect(host='localhost',database='ijh',user='postgres',password='jozH@py4evr',port='5432')
#create cursor
cur=conn.cursor()
try:
    trunc_lz_table="truncate table lz_transaction"
    cur.execute(trunc_lz_table)
    f=open(sys.argv[1],"r")
    l1=[6,6,20,5,7,30,6,4,12,20,11,11,11]
    for x in f:
        l2=[]
        for i in range(len(l1)):
            l2.append(f.read(l1[i]))
        if(x):
            insert_lz_table="INSERT INTO LZ_Transaction (TransactionId, CustomerId, CustomerName, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShipmentDate, DeliveredDate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (l2[0],l2[1],l2[2],l2[3],l2[4],l2[5],l2[6],l2[7],l2[8],l2[9],l2[10],l2[11],l2[12])
            cur.execute(insert_lz_table, val)
    f.close()
    conn.commit()

except Exception as e:
    print("Error:",str(e))
    conn.rollback()

#truncate staging table to accept new data
try:
    trunc_st_table="truncate table st_transaction"
    cur.execute(trunc_st_table)
    conn.commit()

except Exception as e:
    print("Error:",str(e))
    conn.rollback()

#insert into stage table

try:
    insert_st_table="INSERT INTO ST_Transaction SELECT MD5(CONCAT("TransactionId"::text,"CustomerId"::text)),TransactionId, CustomerId, CustomerName, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, to_date(TransactionTimeStamp,'%Y-%m-%e %T'), OrderedDate, ShipmentDate, DeliveredDate FROM LZ_Transaction"
    cur.execute(insert_st_table)

#create a view to join stage and base tables 
    view_st="create view v as selet s.transactionId from st_transaction s inner join base_transaction using transactionId"
    cur.execute(view_st)

#update flags for update and insert
    inorup_st_table="update st_transaction set flag = case when transactionId in ( select transactionId from v) then 'U' else 'I' end"
    cur.execute(inorup_st_table)
    cur.execute("drop view v")
    conn.commit()
except Exception as e:
    print("Error:",str(e))
    print("check if already updated")
    conn.rollback()

#insert into base table
try:
    insert_base_table="insert into Base_Transaction select TransactionId, CustomerId, CustomerNm, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShippedDate, DeliveredDate,activeind from st2_transaction"
    cur.execute(insert_base_table)

#updating active indicator as N for all records which are being updated
    upn_base_table="update base_transaction set activeInd='n' where transactionId in ( select transactionId from st_transaction where flag='u')"
    cur.execute(upn_base_table)

#view for changing activeInd to y
    view_base="create view v as select transactKey,row_number() over (partition by transactionId order by transactionTimeStamp desc,case status when 'delivered' then 1 when 'shipped' then 2 else 3 end) from st_transaction"
    cur.execute(view_base)

#make active indicator as y
    upy_base_table="update base_transaction set activeInd='y' where transactKey in ( select transactKey from st_transaction where transactKey in (select transactKey from v where row_number=1))"
    cur.execute(upy_base_table)
    cur.execute("drop view v")

    conn.commit()

except Exception as e:
    print("Error:",str(e))
    conn.rollback()
cur.close()
conn.close() 
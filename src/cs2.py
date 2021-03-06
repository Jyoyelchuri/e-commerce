#read from daily files and insert in landing zone table
import sys
import datetime
import psycopg2
import string
#connection to database
conn=psycopg2.connect(host='localhost',database='ijh',user='postgres',password='jozH@py4evr',port='5432')
#create cursor
cur=conn.cursor()
aud_key='00000000'
aud_key=datetime.date.today()
try: 
    #store data in audit_key table
    aud_key_table = "INSERT INTO AUDIT_KEY(audit_key,create_dt,source_nm) VALUES(%s,%s,%s)"
    cur.execute(aud_key_table,(aud_key,aud_key,sys.argv[1]))
    
    #commit changes
    conn.commit()

except Exception as e:
    print("Error1 : ", str(e))
    conn.rollback()

try:
    trunc_lz_table="TRUNCATE TABLE LZ_Transaction"
    cur.execute(trunc_lz_table)

    f = open(sys.argv[1], "r")
    l1=[6,6,20,5,7,30,6,4,12,20,11,11,11]
    num_lines=0
    for x in f:
        l2=[]
        current_position = 0
        num_lines+=1
        for i in range(len(l1)):
            end_position = current_position + l1[i]
            l2.append(x[current_position:end_position])
            current_position = end_position
        if(x):
            insert_lz_table = "INSERT INTO LZ_Transaction (TransactionId, CustomerId, CustomerNm, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShippedDate, DeliveredDate,audit_key) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (l2[0],l2[1],l2[2],l2[3],l2[4],l2[5],l2[6],l2[7],l2[8],l2[9],l2[10],l2[11],l2[12],aud_key)
            cur.execute(insert_lz_table, val)
   
    conn.commit()

except Exception as e:
    print("Error 2:",str(e))
    conn.rollback()

#update audit_status for LZ_transaction
try:
    aud_stat_lz_table = "INSERT INTO AUDIT_STATUS(table_nm,audit_key,created_dt,update_dt,source_nm,source_count,target_count,target_insert,target_update) SELECT 'LZ_Transaction',%s,%s,%s,%s,%s,COUNT(*),COUNT(*),0 FROM LZ_Transaction"
    cur.execute(aud_stat_lz_table,(aud_key,aud_key,aud_key, sys.argv[1],num_lines))

    #commit changes
    conn.commit()

except Exception as e:
    print("Error 3: ", str(e))
    conn.rollback()

#truncate staging table to accept new data
try:
    trunc_st_table="truncate table st_transaction"
    cur.execute(trunc_st_table)
    conn.commit()

except Exception as e:
    print("Error 4:",str(e))
    conn.rollback()

#insert into stage table

try:
    insert_st_table="INSERT INTO ST_Transaction(transactkey,TransactionId, CustomerId, CustomerNm, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShippedDate, DeliveredDate,audit_key) SELECT MD5(CONCAT(TransactionId::text,CustomerId::text)),TransactionId, CustomerId, CustomerNm, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, to_date(TransactionTimeStamp,'%Y-%m-%e %T'), OrderedDate, ShippedDate, DeliveredDate,audit_key FROM public.lz_transaction"
    cur.execute(insert_st_table)

#create a view to join stage and base tables 
    view_st="create view v as select s.transactionId from st_transaction s inner join base_transaction b on s.transactionId=b.transactionId"
    cur.execute(view_st)

#update flags for update and insert
    inorup_st_table="update st_transaction set action_ind = case when transactionId in ( select transactionId from v) then 'U' else 'I' end"
    cur.execute(inorup_st_table)
    cur.execute("drop view v")
    conn.commit()
except Exception as e:
    print("Error 5:",str(e))
    conn.rollback()

#update audit_status table for st_transaction
try:
    count_lz= "SELECT COUNT(*) FROM LZ_Transaction"
    cur.execute(count_lz)
    source_count = cur.fetchone()
    
    aud_stat_st_table= "INSERT INTO AUDIT_STATUS(table_nm,audit_key,created_dt,update_dt,source_nm,source_count,target_count,target_insert,target_update) SELECT 'ST_Transaction',%s,%s,%s,'LZ_Transaction',%s,COUNT(*),COUNT(*),0 FROM st_transaction s WHERE audit_key =s.audit_key"
    cur.execute(aud_stat_st_table,(aud_key,aud_key,aud_key,source_count))

    #commit changes
    conn.commit()

except Exception as e:
    print("Error 6: ", str(e))
    conn.rollback()

#insert into base table
try:
    insert_base_table="insert into Base_Transaction(transactkey,TransactionId, CustomerId, CustomerNm, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShippedDate, DeliveredDate,audit_key) select transactkey,TransactionId, CustomerId, CustomerNm, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShippedDate, DeliveredDate,audit_key from st_transaction"
    cur.execute(insert_base_table)

#updating active indicator as N for all records which are being updated
    upn_base_table="update base_transaction set activeInd='n' where transactionId in ( select transactionId from st_transaction where action_ind='u')"
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
    print("Error 7:",str(e))
    conn.rollback()

#update audit status for base_transaction
try:
    count_base_table= "SELECT  COUNT(*) FROM st_transaction "
    cur.execute(count_base_table)
    stg_count = cur.fetchone()
    
    counti_base_tb="SELECT SUM(CASE WHEN action_ind = 'I' THEN 1 ELSE 0 END) AS insert_count FROM st_transaction"
    cur.execute(counti_base_tb)
    base_icount =  cur.fetchone()

    countu_base_tb="SELECT SUM(CASE WHEN action_ind = 'U' THEN 1 ELSE 0 END) AS update_count FROM st_transaction"
    cur.execute(countu_base_tb)
    base_ucount =  cur.fetchone()

    aud_stat_base_table = "INSERT INTO AUDIT_STATUS(Table_nm,Audit_key,created_dt,update_dt,Source_nm,Source_count,Target_count,Target_insert,Target_update) SELECT 'BASE_Transaction',%s,%s,%s,'ST_Transaction',%s,COUNT(*),%s,%s FROM BASE_Transaction b WHERE Audit_key = b.audit_key"
    cur.execute(aud_stat_base_table,(aud_key,aud_key,aud_key,stg_count,base_icount,base_ucount))
	
    #status update
    up_aud_stat= "UPDATE AUDIT_STATUS SET Status= CASE WHEN Source_count = Target_count THEN 'M' ELSE 'F' END"
    cur.execute(up_aud_stat)

    #commit changes
    conn.commit()

except Exception as e:
    print("Error 8: ", str(e))
    conn.rollback()


cur.close()
conn.close() 
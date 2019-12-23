import sys
import psycopg2

conn = psycopg2.connect(
  database="db",
  user="postgres",
  password="jozH@py4evr",
  host="localhost",
  port="5432"
)

cur=conn.cursor()
try:

    values = []
    trunc_lz_table="TRUNCATE TABLE LZ_Transaction"
    cur.execute(trunc_lz_table)

    f = open(sys.argv[1], "r")
    l1=[6,6,20,5,7,30,6,4,12,20,11,11,11]
    for x in f:
        l2=[]	
        for i in range(len(l1)):
    	    l2.append(f.read(l1[i]))
        if(x):
            insert_lz_table = "INSERT INTO LZ_Transaction (TransactionId, CustomerId, CustomerName, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShipmentDate, DeliveredDate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (l2[0],l2[1],l2[2],l2[3],l2[4],l2[5],l2[6],l2[7],l2[8],l2[9],l2[10],l2[11],l2[12])
            cur.execute(insert_lz_table, val)
    f.close()
    conn.commit()

    insert_st_table="INSERT INTO ST_Transaction SELECT TransactionId, CustomerId, CustomerName, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, to_date(TransactionTimeStamp,'%Y-%m-%e %T'), OrderedDate, ShipmentDate, DeliveredDate FROM LZ_Transaction"
    cur.execute(insert_st_table)

    update_st_table="update ST_Transaction set ActiveInd='y'"
    cur.execute(update_st_table)

    temp_st_table="insert into st2_transaction select * from ( select * , ROW_NUMBER () over (partition by TransactionId order by TransactionTimeStamp desc,case when Status='Delivered   ' then 3 when status='Shipped     ' then 2 when status='Ordered     'then 1 else 0 end) as rownum  from ST_Transaction) s" 
    cur.execute(temp_st_table)

    update_temp_st_table="UPDATE st2_transaction SET activeInd='N' where rownum > 1"
    cur.execute(update_temp_st_table)

    insert_base_table="insert into Base_Transaction select TransactionId, CustomerId, CustomerNm, CustomerAddrId, ProductId, ProductNm, ProductPrice, ProductQuantity, Status, TransactionTimeStamp, OrderedDate, ShippedDate, DeliveredDate,activeind from st2_transaction"
    cur.execute(insert_base_table)
    conn.commit()

except Exception as e:
    print("Error:",str(e))
    conn.rollback()

cur.close()
conn.close() 



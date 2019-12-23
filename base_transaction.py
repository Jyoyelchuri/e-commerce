CREATE TABLE public.base_transaction
(
    "TransactionId" character(6) COLLATE pg_catalog."default",
    "CustomerId" character(6) COLLATE pg_catalog."default",
    "CustomerNm" character(20) COLLATE pg_catalog."default",
    "CustomerAddrId" character(5) COLLATE pg_catalog."default",
    "ProductId" character(7) COLLATE pg_catalog."default",
    "ProductNm" character(30) COLLATE pg_catalog."default",
    "ProductPrice" character(6) COLLATE pg_catalog."default",
    "ProductQuantity" character(4) COLLATE pg_catalog."default",
    status character(12) COLLATE pg_catalog."default",
    "TransactionTimeStamp" timestamp(6) with time zone,
    "OrderedDate" character(11) COLLATE pg_catalog."default",
    "ShippedDate" character(11) COLLATE pg_catalog."default",
    "DeliveredDate" character(11) COLLATE pg_catalog."default",
    "ActiveInd" character(1) COLLATE pg_catalog."default",
    seqnum integer NOT NULL DEFAULT nextval('base_transaction_seqnum_seq'::regclass)
)

TABLESPACE pg_default;

ALTER TABLE public.base_transaction
    OWNER to postgres;
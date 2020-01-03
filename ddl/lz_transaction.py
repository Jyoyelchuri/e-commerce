CREATE TABLE public.lz_transaction
(
    transactionid character(6) COLLATE pg_catalog."default",
    customerid character(6) COLLATE pg_catalog."default",
    customernm character(20) COLLATE pg_catalog."default",
    customeraddrid character(5) COLLATE pg_catalog."default",
    productid character(7) COLLATE pg_catalog."default",
    productnm character(30) COLLATE pg_catalog."default",
    productprice character(6) COLLATE pg_catalog."default",
    productquantity character(4) COLLATE pg_catalog."default",
    status character(12) COLLATE pg_catalog."default",
    transactiontimestamp character(20) COLLATE pg_catalog."default",
    ordereddate character(11) COLLATE pg_catalog."default",
    shippeddate character(11) COLLATE pg_catalog."default",
    delivereddate character(11) COLLATE pg_catalog."default",
    audit_key date
)

TABLESPACE pg_default;

ALTER TABLE public.lz_transaction
    OWNER to postgres;
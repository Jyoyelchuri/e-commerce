CREATE TABLE public.st_transaction
(
    transactkey character varying COLLATE pg_catalog."default",
    transactionid character(6) COLLATE pg_catalog."default",
    customerid character(6) COLLATE pg_catalog."default",
    customernm character(20) COLLATE pg_catalog."default",
    customeraddrid character(5) COLLATE pg_catalog."default",
    productid character(7) COLLATE pg_catalog."default",
    productnm character(30) COLLATE pg_catalog."default",
    productprice character(6) COLLATE pg_catalog."default",
    productquantity character(4) COLLATE pg_catalog."default",
    status character(12) COLLATE pg_catalog."default",
    transactiontimestamp timestamp(6) without time zone,
    ordereddate character(11) COLLATE pg_catalog."default",
    shippeddate character(11) COLLATE pg_catalog."default",
    delivereddate character(11) COLLATE pg_catalog."default",
    action_ind character(1) COLLATE pg_catalog."default",
    audit_key date
)

TABLESPACE pg_default;

ALTER TABLE public.st_transaction
    OWNER to postgres;
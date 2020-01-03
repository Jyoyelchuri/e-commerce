CREATE SEQUENCE public.base_transaction_seqnum_seq
    INCREMENT 1
    START 214
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.base_transaction_seqnum_seq
    OWNER TO postgres;
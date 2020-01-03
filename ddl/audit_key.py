CREATE TABLE public.audit_key
(
    audit_key date NOT NULL,
    create_dt date,
    source_nm character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.audit_key
    OWNER to postgres;
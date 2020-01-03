CREATE TABLE public.audit_status
(
    table_nm character varying COLLATE pg_catalog."default",
    created_dt date,
    update_dt date,
    source_nm character varying COLLATE pg_catalog."default",
    source_count integer,
    target_count integer,
    target_insert integer,
    target_update integer,
    status character varying COLLATE pg_catalog."default",
    audit_key date
)

TABLESPACE pg_default;

ALTER TABLE public.audit_status
    OWNER to postgres;
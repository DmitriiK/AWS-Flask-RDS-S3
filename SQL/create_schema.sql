CREATE TABLE public.S3_Files
(
    Id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    PublicUrl character varying(500)  NOT NULL,
    FileName character varying(100)  NOT NULL,
    Created_At timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT S3_Ffiles_pkey PRIMARY KEY (Id)
)
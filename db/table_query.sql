CREATE TABLE public."user"
(
    id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    username character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    password character varying(200) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_email_key UNIQUE (email),
    CONSTRAINT user_username_key UNIQUE (username)
)

TABLESPACE pg_default;

ALTER TABLE public."user"
    OWNER to postgres;
	
INSERT INTO user(username,email,password) 
values('Ericsson','cericsson1@vinaora.com','sha256$dVGrf2jxFEUYGBkV$1d38b13c6f16dbfe4604a0a2479ae975f6893d1adba1fadea49c70669ed597a4');
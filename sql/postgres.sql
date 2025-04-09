-- SETUP

CREATE TABLE debezium.public.dw_currency(  
    id  UUID NOT NULL DEFAULT gen_random_uuid(),
    create_time TIMESTAMP null DEFAULT now(),
    currency_date DATE null,
    currency_code VARCHAR(32) null,
    currency_name VARCHAR(32) null,
    value_to_try FLOAT null
);

ALTER TABLE dw_currency REPLICA IDENTITY FULL;

-- TEST

insert into debezium.public.dw_currency (currency_date, currency_code, currency_name, value_to_try) values ('2025-04-08', 'DUM', 'DUM Dummy', -3);

update debezium.public.dw_currency
set value_to_try=-5
where value_to_try=-3;

delete from debezium.public.dw_currency
where value_to_try=-5;


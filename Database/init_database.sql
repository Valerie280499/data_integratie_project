-- Description: script that initializes the database upon building the Docker container
-- Author: Anne Manders
-- Version: 3
-- Date: 10-06-2020

CREATE DATABASE data_integratie;

USE data_integratie;

CREATE TABLE variant (
    variant_id            VARCHAR(20) NOT NULL,
    chromosome             VARCHAR(10),
    position               INTEGER,
    reference              VARCHAR(10),
    alternative            VARCHAR(10),
    variant_type			VARCHAR(10),
    cancer_alt_allele_frequency			FLOAT
);

ALTER TABLE variant ADD CONSTRAINT variant_pk PRIMARY KEY ( variant_id );
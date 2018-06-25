### DB schema

(I understood from course requirements that CREATE TABLE statements should also
be included in documentation...?)

```sql
CREATE TABLE shareholder (
    id VARCHAR(32) PRIMARY KEY,
    city VARCHAR(64) NOT NULL,
    created_on DATETIME,
    country VARCHAR(64) NOT NULL,
    email VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    has_access BOOLEAN NOT NULL,
    pw_hash VARCHAR(64) NOT NULL,
    street VARCHAR(255) NOT NULL,
    street_ext VARCHAR(255),
    type VARCHAR(16),
    updated_on DATETIME,
    zip_code VARCHAR(32) NOT NULL,
    UNIQUE (email)
);
CREATE TABLE juridical_person (
    id VARCHAR(32) PRIMARY KEY,
    business_id VARCHAR(32) NOT NULL,
    contact_person VARCHAR(128) NOT NULL,
    name VARCHAR(128) NOT NULL,
    FOREIGN KEY (id) REFERENCES shareholder (id),
    UNIQUE (business_id)
);
CREATE TABLE natural_person (
    id VARCHAR(32) PRIMARY KEY,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    nationality VARCHAR(64) NOT NULL,
    nin VARCHAR(16) NOT NULL,
    FOREIGN KEY (id) REFERENCES shareholder (id)
);
CREATE TABLE share_class (
    id VARCHAR(32) PRIMARY KEY,
    created_on DATETIME,
    name VARCHAR(32) NOT NULL,
    remarks VARCHAR(255),
    updated_on DATETIME,
    votes INTEGER NOT NULL,
    UNIQUE (name)
);
CREATE TABLE share (
    id BIGINT PRIMARY KEY,
    share_class_id VARCHAR(32) NOT NULL,
    canceled_on DATE,
    created_on DATETIME,
    is_bound BOOLEAN NOT NULL,
    issued_on DATE NOT NULL,
    updated_on DATETIME,
    FOREIGN KEY (share_class_id) REFERENCES share_class (id)
);
CREATE TABLE certificate (
    id VARCHAR(32) PRIMARY KEY,
    owner_id VARCHAR(32) NOT NULL,
    canceled_on DATE,
    created_on DATETIME,
    first_share BIGINT NOT NULL,
    issued_on DATE NOT NULL,
    last_share BIGINT NOT NULL,
    share_count BIGINT NOT NULL,
    updated_on DATETIME,
    FOREIGN KEY (owner_id) REFERENCES shareholder (id)
);
CREATE TABLE _transaction (
    id VARCHAR(32) PRIMARY KEY,
    buyer_id VARCHAR(32) NOT NULL,
    certificate_id VARCHAR(32) NOT NULL,
    seller_id VARCHAR(32) NOT NULL,
    created_on DATETIME,
    price BIGINT,
    price_per_share BIGINT,
    recorded_on DATE NOT NULL,
    remarks VARCHAR(255),
    updated_on DATETIME,
    FOREIGN KEY (buyer_id) REFERENCES shareholder (id),
    FOREIGN KEY (certificate_id) REFERENCES certificate (id),
    FOREIGN KEY (seller_id) REFERENCES shareholder (id)
);
CREATE TABLE certificate_share (
    certificate_id VARCHAR(32),
    share_id BIGINT,
    FOREIGN KEY (certificate_id) REFERENCES certificate (id),
    FOREIGN KEY (share_id) REFERENCES share (id)
);
```
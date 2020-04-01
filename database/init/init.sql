
BEGIN;

CREATE TABLE movies (
    m_id VARCHAR(16) PRIMARY KEY,
    title VARCHAR(128) NOT NULL
);

CREATE TABLE users (
    u_id SERIAL PRIMARY KEY,
    u_name VARCHAR(32) NOT NULL UNIQUE,
    pass_hash VARCHAR(128) NOT NULL,
    email VARCHAR(64) UNIQUE NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE u_tasks (
    u_id INTEGER NOT NULL,
    m_id VARCHAR(16) NOT NULL,
    requested_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (u_id, m_id),
    CONSTRAINT u_tasks_u_id_fkey FOREIGN KEY (u_id)
        REFERENCES users (u_id) MATCH SIMPLE
        ON UPDATE RESTRICT ON DELETE CASCADE,
    CONSTRAINT u_tasks_m_id_fkey FOREIGN KEY (m_id)
        REFERENCES movies (m_id) MATCH SIMPLE
        ON UPDATE RESTRICT ON DELETE CASCADE
);

CREATE TABLE workers (
    w_id SERIAL PRIMARY KEY,
    ip_address INET NOT NULL,
    domain_name VARCHAR(128) NOT NULL
);

CREATE TABLE w_tasks (
    m_id VARCHAR(16) NOT NULL,
    w_id INTEGER DEFAULT 1,
    status VARCHAR(16) NOT NULL DEFAULT 'WAIT',
    url VARCHAR(256) DEFAULT NULL,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (m_id, w_id),
    CONSTRAINT w_tasks_m_id_fkey FOREIGN KEY (m_id)
        REFERENCES movies (m_id) MATCH SIMPLE
        ON UPDATE RESTRICT ON DELETE CASCADE,
    CONSTRAINT w_tasks_w_id_fkey FOREIGN KEY (w_id)
        REFERENCES workers (w_id) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE roles (
   r_id SERIAL PRIMARY KEY,
   r_name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE u_roles (
    u_id INTEGER NOT NULL,
    r_id INTEGER NOT NULL,
    PRIMARY KEY (u_id, r_id),
    CONSTRAINT u_role_u_id_fkey FOREIGN KEY (u_id)
        REFERENCES users (u_id) MATCH SIMPLE
        ON UPDATE RESTRICT ON DELETE CASCADE,
    CONSTRAINT u_role_r_id_fkey FOREIGN KEY (r_id)
        REFERENCES roles (r_id) MATCH SIMPLE
        ON UPDATE RESTRICT ON DELETE CASCADE
);

COMMIT;

BEGIN;

CREATE OR REPLACE FUNCTION template (

) AS
$BODY$
BEGIN

END;
$BODY$
    LANGUAGE 'plpgsql' VOLATILE;

CREATE OR REPLACE FUNCTION add_u_task (
    in user_id integer, in movie_id text,
    out task_status text
) AS
$BODY$ 
BEGIN
INSERT INTO u_tasks (u_id, m_id)
VALUES (user_id, movie_id);
SELECT status
  INTO task_status
  FROM w_tasks
 WHERE m_id=movie_id;
if task_status is NULL then
  task_status='NEW';
end if;
END;
$BODY$
    LANGUAGE 'plpgsql' VOLATILE;



COMMIT;

/*---------------------------------------------------------------------
// Name:    Eric Stanton, Andrew Kaiser, Stephen Stirling
// Class:   CS 3630: Database Design and Implementation
// Project: Course Project
// Purpose: Create and populate the User Database Management System
//-------------------------------------------------------------------*/

-- Drop all tables
DROP TABLE IF EXISTS states CASCADE;
DROP TABLE IF EXISTS addresses CASCADE;
DROP TABLE IF EXISTS contact_information CASCADE;
DROP TABLE IF EXISTS contact_relationships CASCADE;
DROP TABLE IF EXISTS emergency_contacts CASCADE;
DROP TABLE IF EXISTS user_data CASCADE;
DROP TABLE IF EXISTS user_types CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS shift_roles CASCADE;
DROP TABLE IF EXISTS shifts CASCADE;
DROP TABLE IF EXISTS job_titles CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS staff CASCADE;

DROP FUNCTION IF EXISTS updated();

CREATE FUNCTION updated() RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$$
BEGIN
    NEW.updated_at := current_timestamp;
    RETURN NEW;
END;
$$;

------------------------------------------------------------------------
-- The Left side of the ERD - Address Stuff
------------------------------------------------------------------------

--Creates the states that may be associated with Addresses
CREATE TABLE states
(
    id                 integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    state_abbreviation varchar(2)               NOT NULL UNIQUE,
    created_at         timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at         timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted            boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_states_updated
    BEFORE UPDATE
    ON states
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO states (state_abbreviation)
VALUES ('AL'),
       ('AK'),
       ('AZ'),
       ('AR'),
       ('CA'),
       ('CO'),
       ('CT'),
       ('DE'),
       ('FL'),
       ('GA'),
       ('HI'),
       ('ID'),
       ('IL'),
       ('IN'),
       ('IA'),
       ('KS'),
       ('KY'),
       ('LA'),
       ('ME'),
       ('MD'),
       ('MA'),
       ('MI'),
       ('MN'),
       ('MS'),
       ('MO'),
       ('MT'),
       ('NE'),
       ('NV'),
       ('NH'),
       ('NJ'),
       ('NM'),
       ('NY'),
       ('NC'),
       ('ND'),
       ('OH'),
       ('OK'),
       ('OR'),
       ('PA'),
       ('RI'),
       ('SC'),
       ('SD'),
       ('TN'),
       ('TX'),
       ('UT'),
       ('VT'),
       ('VA'),
       ('WA'),
       ('WV'),
       ('WI'),
       ('WY');


--Creates the Addresses associated with a contact's information and potentially an emergency contact
CREATE TABLE addresses
(
    id                   integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    street               varchar(50)              NOT NULL,
    city                 varchar(255)             NOT NULL,
    states_id            integer                  NOT NULL REFERENCES states (id) DEFERRABLE,
    postal_code          varchar(5)               NOT NULL,
    country_abbreviation varchar(2)               NOT NULL,
    created_at           timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at           timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted              boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_addresses_updated
    BEFORE UPDATE
    ON addresses
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO addresses (street, city, states_id, postal_code, country_abbreviation)
VALUES ('4891 Brownton Road', 'Meridian', 49, '39301', 'US'),
       ('4215 Langtown Road', 'Davenport', 14, '52801', 'US'),
       ('2896 Ferry Street', 'Huntsville', 34, '35816', 'US'),
       ('4336 Richards Avenue', 'Stockton', 49, '95202', 'US'),
       ('1044 Bubby Drive', 'Austin', 49, '78701', 'US');


------------------------------------------------------------------------
-- The Left side of the ERD - User_data Contact stuff
------------------------------------------------------------------------


--Creates the contact information related to user data
CREATE TABLE contact_information
(
    id           integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email        varchar(50)              NOT NULL UNIQUE,
    phone_number varchar(15)              NOT NULL,
    address_id   integer                  NOT NULL REFERENCES addresses (id) DEFERRABLE,
    created_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted      boolean                  NOT NULL DEFAULT false
);

INSERT INTO contact_information (email, phone_number, address_id)
VALUES ('MarieMLindsey@gmail.com', '+16623595178', 1),
       ('BrianDHoward@gmail.com', '+12567011099', 3),
       ('TracyDZimmerman@live.com', '+12099427708', 4),
       ('MadisonLTayolor@gmail.com', '+15123821200', 5);

CREATE TRIGGER trigger_contact_information_updated
    BEFORE UPDATE
    ON contact_information
    FOR EACH ROW
EXECUTE PROCEDURE updated();

--Creates the contact_relationship used in Emergency Contacts
CREATE TABLE contact_relationships
(
    id         integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    type       varchar(20)              NOT NULL UNIQUE,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted    boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_contact_relationships_updated
    BEFORE UPDATE
    ON contact_relationships
    FOR EACH ROW
EXECUTE PROCEDURE updated();


INSERT INTO contact_relationships (type)
VALUES ('parent'),
       ('guardian'),
       ('sibling'),
       ('spouse'),
       ('friend'),
       ('other');


--Creates the emergency contact related to user data
CREATE TABLE emergency_contacts
(
    id                      integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    first_name              varchar(50)              NOT NULL,
    last_name               varchar(50)              NOT NULL,
    contact_relationship_id integer                  NOT NULL REFERENCES contact_relationships (id) DEFERRABLE,
    email                   varchar(50) UNIQUE,
    phone_number            varchar(15)              NOT NULL,
    address_id              integer REFERENCES addresses (id),
    created_at              timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at              timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted                 boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_emergency_contacts_updated
    BEFORE UPDATE
    ON emergency_contacts
    FOR EACH ROW
EXECUTE PROCEDURE updated();


INSERT INTO emergency_contacts (first_name, last_name, contact_relationship_id, email, phone_number, address_id)
VALUES ('Ashley', 'Sears', 5, 'AshleyJSears@gmail.com', '563-663-2496', 2),
       ('Teresa', 'Howard', 4, 'TeresaRCastle@gmail.com', '352-796-8406', 3),
       ('Diane', 'Taylor', 5, 'DTaylor12@gmail.com', '908-359-0173', 5),
       ('Don', 'Zimmerman', 4, 'DonSZimmerman@gmail.com', '908-359-0172', 4);

--Creates the users data related to users
CREATE TABLE user_data
(
    id                     integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    first_name             varchar(50)              NOT NULL,
    last_name              varchar(50)              NOT NULL,
    date_of_birth          date                     NOT NULL,
    contact_information_id integer                  NOT NULL REFERENCES contact_information (id) DEFERRABLE,
    emergency_contact_id   integer REFERENCES emergency_contacts (id),
    created_at             timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at             timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted                boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_user_data_updated
    BEFORE UPDATE
    ON user_data
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO user_data (first_name, last_name, date_of_birth, contact_information_id, emergency_contact_id)
VALUES ('Marie', 'Lindsey', '1965-9-10', 1, 1),
       ('Brian', 'Howard', '1971-1-28', 2, 2),
       ('Madison', 'Taylor', '1984-5-22', 4, 3),
       ('Tracy', 'Zimmerman', '1990-3-16', 3, 4);


------------------------------------------------------------------------
-- The center of the ERD : USER
------------------------------------------------------------------------


--Creates the user's privilege role/profile/type to access the system. Related to users.
CREATE TABLE user_types
(
    id         integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    role       varchar(50)              NOT NULL UNIQUE,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted    boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_user_types_updated
    BEFORE UPDATE
    ON user_types
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO user_types (role)
VALUES ('employee'),
       ('volunteer'),
       ('administrator');


--Creates the master table where user's are created, updated, and modified
CREATE TABLE users
(
    id           integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username     varchar(20)              NOT NULL UNIQUE,
    pin          varchar(4)               NOT NULL,
    user_type_id integer                  NOT NULL REFERENCES user_types (id) DEFERRABLE,
    created_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted      boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_users_updated
    BEFORE UPDATE
    ON users
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO users (username, pin, user_type_id)
VALUES ('LindseyM', '1111', 1),
       ('HowardB', 'ZRS7', 3),
       ('TaylorM', '2222', 1),
       ('TracyZ', '3333', 2);


------------------------------------------------------------------------
-- The Right side of the ERD - Tables for User position and work
------------------------------------------------------------------------


--Creates the building table used in shift_role
CREATE TABLE buildings
(
    id         integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name       varchar(50)              NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted    boolean                  NOT NULL DEFAULT false
);
CREATE INDEX index_building_name ON buildings (name);


CREATE TRIGGER trigger_buildings_updated
    BEFORE UPDATE
    ON buildings
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO buildings (name)
VALUES ('Warner Administration Complex'),
       ('Greenhouse'),
       ('Conservation Learning Center'),
       ('Train Station'),
       ('Café'),
       ('Gift Shop'),
       ('Marangu Trail Outpost'),
       ('Otto Center'),
       ('Owens Aviary'),
       ('Warner Plaza');


--Creates the role table used to assign task + locations if Zoo section implemented
--otherwise it states the text needed to do the task.
CREATE TABLE roles
(
    id               integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title            varchar(50)              NOT NULL,
    responsibilities text                     NOT NULL,
    created_at       timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at       timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted          boolean                  NOT NULL DEFAULT false
);
CREATE INDEX index_role_title ON roles (title);


CREATE TRIGGER trigger_roles_updated
    BEFORE UPDATE
    ON roles
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO roles (title, responsibilities)
VALUES ('Animal Curator',
        'Manages some or all of an institution''s animal collection. For instance, there may be a curator of mammals, or a curator of rainforest species.'),
       ('General Curator',
        'Oversees an institution''s entire animal collection and animal management staff. Responsible for strategic collection planning.'),
       ('Curator of Exhibits', 'Creates exhibits and assists in the design of graphics.'),
       ('Curator of Horticulture',
        'Responsible for the botanical collection and its application to the animal collection, as well as daily maintenance of the institution''s grounds.'),
       ('Curator of Education', 'Plans and implements the institution''s education programs.'),
       ('Curator of Research',
        'Supervises research projects, serves as liaison between the institution and the academic community, and publishes articles in scientific journals.'),
       ('Curator of Conservation',
        'Oversees the institution''s conservation activities, including field projects. Serves as liaison with government wildlife agencies and other conservation organizations.'),
       ('Zoo Director',
        'Executes policies as directed by the governing authority. Responsible for the institution''s operation and plans for future development.'),
       ('Assistant Director', 'Assists the director and assumes charge in the director''s absence.'),
       ('Finance Director',
        'Manages the institution''s finances, including payment of bills, purchasing, investments, and the preparation of financial statements.'),
       ('Public Relations Director',
        'Promotes the institution, its mission, and its programs to the public via the media.'),
       ('Development Director',
        'Develops and manages fund-raising activities which can include writing grant proposals and attracting corporate sponsors, as well as soliciting private donations.'),
       ('Marketing Director',
        'Creates advertising campaigns and other activities to increase public awareness of the institution.'),
       ('Special Events Manager', 'Develops and implements events to attract visitors throughout the year.'),
       ('Membership Director',
        'Responsible for maintaining and increasing institution memberships for families and individuals and designing special events for members only. May also be in charge of adopt-an-animal programs to raise funds.'),
       ('Personnel Manager', 'Responsible for all personnel matters including payroll, insurance, and tax matters.'),
       ('Operations Director',
        'Responsible for the daily operation of the institution''s physical plant and equipment.'),
       ('Head Keeper',
        'Supervises a section or department of the institution; provides training and scheduling for keepers.'),
       ('Assistant Keeper',
        'Supervises a section or department of the institution; provides training and scheduling for keepers.'),
       ('Lead System Administrator', 'Supervises the sytsem administrators; Handles the management of the system'),
       ('Lead Veterinarian',
        'Responsible for the healthcare program for the animal collection and the maintenance of health records.');

--Creates the shift_role used in shifts. The role and building being assigned.
CREATE TABLE shift_roles
(
    id          integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    role_id     integer                  NOT NULL REFERENCES roles (id) DEFERRABLE,
    building_id integer REFERENCES buildings (id),
    created_at  timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at  timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted     boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_shift_roles_updated
    BEFORE UPDATE
    ON shift_roles
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO shift_roles (role_id, building_id)
VALUES (21, 8),
       (21, 9),
       (20, 1),
       (19, 9),
       (19, 7),
       (19, 10),
       (11, 5),
       (4, 3);

--Creates the Job Title table associated with a Job.
CREATE TABLE job_titles
(
    id              integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name            varchar(50)              NOT NULL UNIQUE,
    job_description text                     NOT NULL,
    full_time       boolean                  NOT NULL,
    created_at      timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at      timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted         boolean                  NOT NULL DEFAULT false
);
CREATE INDEX index_job_name ON job_titles (name);


CREATE TRIGGER trigger_job_titles_updated
    BEFORE UPDATE
    ON job_titles
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO job_titles (name, job_description, full_time)
VALUES ('Veterinarian',
        'Responsible for the healthcare program for the animal collection and the maintenance of health records.',
        TRUE),
       ('Veterinary Technician',
        'Assists the veterinarian and provides care to the animals under the supervision of the veterinarian.', TRUE),
       ('Curator',
        'Oversees an institution''s entire animal collection and animal management staff. Responsible for strategic collection planning.',
        TRUE),
       ('Conservation Zoologist',
        'Provides scientific and technical assistance in the management of the animal collection and assists in conducting various research or field conservation projects.',
        FALSE),
       ('Conservation Biologist',
        'Provides scientific and technical assistance in the management of the animal collection and assists in conducting various research or field conservation projects.',
        FALSE),
       ('Keeper',
        'Provides daily care to the institution''s animals, including diet preparation, cleaning, general exhibit maintenance, and recordkeeping.',
        TRUE),
       ('Registrar',
        'Maintains computer records on the animal collection and applies for permits and licenses to hold or transport animals.',
        TRUE),
       ('Gift Shop Manager',
        'Manages staff and all aspects of gift shop operation from buying products to designing shops.', TRUE),
       ('Volunteer Coordinator',
        'Responsible for recruiting and maintaining a staff of volunteers/docents. Duties include scheduling docents for on- and off-grounds activities and keeping docents abreast of new developments to relate to the public.',
        TRUE),
       ('System Administrator',
        'Support and administer third party applications, Monitor and Maintain network security and connectivity, Maintain network performance, Set up user accounts, permissions, passwords.',
        TRUE);


--Creates the Job given to an Employee or Volunteer
CREATE TABLE jobs
(
    id           integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    job_title_id integer                  NOT NULL REFERENCES job_titles (id) DEFERRABLE,
    salary       numeric(8, 0)            NOT NULL,
    created_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted      boolean                  NOT NULL DEFAULT false,
    check (salary > 0)
);


CREATE TRIGGER trigger_jobs_updated
    BEFORE UPDATE
    ON jobs
    FOR EACH ROW
EXECUTE PROCEDURE updated();


INSERT INTO jobs (job_title_id, salary)
VALUES (10, 70500),
       (6, 25800),
       (1, 103570),
       (3, 46452);


--Creates an Employee associated with a Users, jobs, and work_schedule.
CREATE TABLE staff
(
    id           integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id      integer                  NOT NULL UNIQUE REFERENCES users (id) DEFERRABLE,
    job_id       integer                  NOT NULL REFERENCES jobs (id) DEFERRABLE,
    user_data_id integer                  NOT NULL REFERENCES user_data (id) UNIQUE DEFERRABLE,
    created_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at   timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted      boolean                  NOT NULL DEFAULT false
);

CREATE TRIGGER trigger_staff_updated
    BEFORE UPDATE
    ON staff
    FOR EACH ROW
EXECUTE PROCEDURE updated();

INSERT INTO staff (user_id, job_id, user_data_id)
VALUES (1, 3, 1),
       (2, 2, 2),
       (3, 1, 3),
       (4, 4, 4);


--Creates the Shift table used in work_schedule. Used to store shift times and tasks associated to the shift
CREATE TABLE shifts
(
    id            integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    staff_id      integer                  NOT NULL REFERENCES staff (id) DEFERRABLE,
    date          date                     NOT NULL,
    start_time    time                     NOT NULL,
    end_time      time                     NOT NULL,
    clock_in      time,
    clock_out     time,
    shift_role_id integer                  NOT NULL REFERENCES shift_roles (id) DEFERRABLE,
    created_at    timestamp with time zone NOT NULL DEFAULT current_timestamp,
    updated_at    timestamp with time zone NOT NULL DEFAULT current_timestamp,
    deleted       boolean                  NOT NULL DEFAULT false
);
CREATE INDEX index_shift_date ON shifts (date);
CREATE INDEX index_shift_start ON shifts (start_time);
CREATE INDEX index_shift_end ON shifts (end_time);

CREATE TRIGGER trigger_shifts_updated
    BEFORE UPDATE
    ON shifts
    FOR EACH ROW
EXECUTE PROCEDURE updated();

--Insertinf data for a user that has worked for a week
INSERT INTO shifts (staff_id, date, start_time, end_time, clock_in, clock_out, shift_role_id)
VALUES (1, '2020-5-11', '08:00:00', '14:00:00', '07:59:00', '14:00:00', 1),
       (1, '2020-5-12', '08:00:00', '14:00:00', '07:59:00', '14:00:00', 1),
       (1, '2020-5-13', '08:00:00', '14:00:00', '07:59:00', '14:00:00', 1),
       (1, '2020-5-14', '08:00:00', '14:00:00', '07:59:00', '14:00:00', 1),
       (1, '2020-5-15', '08:00:00', '14:00:00', '07:59:00', '14:00:00', 1),
       (2, '2020-5-16', '08:00:00', '14:00:00', '07:59:00', '14:15:00', 3);


--Insertinf data for a future shcedule
INSERT INTO shifts (staff_id, date, start_time, end_time, shift_role_id)
VALUES (2, '2020-5-25', '08:00:00', '14:00:00', 3),
       (3, '2020-5-25', '08:00:00', '14:00:00', 4),
       (1, '2020-5-26', '08:00:00', '14:00:00', 2),
       (2, '2020-5-26', '08:00:00', '14:00:00', 3),
       (3, '2020-5-26', '08:00:00', '14:00:00', 5),
       (4, '2020-5-26', '08:00:00', '14:00:00', 7),
       (1, '2020-5-27', '08:00:00', '14:00:00', 1),
       (2, '2020-5-27', '08:00:00', '14:00:00', 3),
       (3, '2020-5-27', '08:00:00', '14:00:00', 6),
       (1, '2020-5-28', '08:00:00', '14:00:00', 2),
       (2, '2020-5-28', '08:00:00', '14:00:00', 3),
       (3, '2020-5-28', '08:00:00', '14:00:00', 4),
       (1, '2020-5-29', '08:00:00', '14:00:00', 1),
       (2, '2020-5-29', '08:00:00', '14:00:00', 3),
       (3, '2020-5-29', '08:00:00', '14:00:00', 5),
       (4, '2020-5-30', '10:00:00', '11:00:00', 8),
       (3, '2020-5-30', '10:00:00', '11:00:00', 5);


------------------------------------------------------------------------------------------------------------------------
-- //ToDo: Trigger between hours_worked and work_schedule : Everytime a shift is updated update the hours_worked table.
------------------------------------------------------------------------------------------------------------------------

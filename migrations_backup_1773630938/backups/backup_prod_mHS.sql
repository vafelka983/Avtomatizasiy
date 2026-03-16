--
-- PostgreSQL database dump
--

\restrict yMNSJhFkg9QmPxxMWOeicO4reeIGzVMdQVoS4unnhAih3LieyS6a74GTDC6mViC

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO avtomat_user;

--
-- Name: boats; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.boats (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    boat_type character varying(50),
    displacement double precision,
    build_date date,
    engine_power integer,
    fuel_capacity double precision
);


ALTER TABLE public.boats OWNER TO avtomat_user;

--
-- Name: boats_id_seq; Type: SEQUENCE; Schema: public; Owner: avtomat_user
--

CREATE SEQUENCE public.boats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.boats_id_seq OWNER TO avtomat_user;

--
-- Name: boats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avtomat_user
--

ALTER SEQUENCE public.boats_id_seq OWNED BY public.boats.id;


--
-- Name: catches; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.catches (
    id integer NOT NULL,
    trip_ground_id integer NOT NULL,
    fish_species_id integer NOT NULL,
    weight double precision NOT NULL
);


ALTER TABLE public.catches OWNER TO avtomat_user;

--
-- Name: catches_id_seq; Type: SEQUENCE; Schema: public; Owner: avtomat_user
--

CREATE SEQUENCE public.catches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.catches_id_seq OWNER TO avtomat_user;

--
-- Name: catches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avtomat_user
--

ALTER SEQUENCE public.catches_id_seq OWNED BY public.catches.id;


--
-- Name: crew_members; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.crew_members (
    id integer NOT NULL,
    trip_id integer NOT NULL,
    full_name character varying(150) NOT NULL,
    address text,
    "position" character varying(50)
);


ALTER TABLE public.crew_members OWNER TO avtomat_user;

--
-- Name: crew_members_id_seq; Type: SEQUENCE; Schema: public; Owner: avtomat_user
--

CREATE SEQUENCE public.crew_members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.crew_members_id_seq OWNER TO avtomat_user;

--
-- Name: crew_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avtomat_user
--

ALTER SEQUENCE public.crew_members_id_seq OWNED BY public.crew_members.id;


--
-- Name: fish_species; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.fish_species (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.fish_species OWNER TO avtomat_user;

--
-- Name: fish_species_id_seq; Type: SEQUENCE; Schema: public; Owner: avtomat_user
--

CREATE SEQUENCE public.fish_species_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fish_species_id_seq OWNER TO avtomat_user;

--
-- Name: fish_species_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avtomat_user
--

ALTER SEQUENCE public.fish_species_id_seq OWNED BY public.fish_species.id;


--
-- Name: fishing_grounds; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.fishing_grounds (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    latitude double precision,
    longitude double precision,
    depth double precision
);


ALTER TABLE public.fishing_grounds OWNER TO avtomat_user;

--
-- Name: fishing_grounds_id_seq; Type: SEQUENCE; Schema: public; Owner: avtomat_user
--

CREATE SEQUENCE public.fishing_grounds_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fishing_grounds_id_seq OWNER TO avtomat_user;

--
-- Name: fishing_grounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avtomat_user
--

ALTER SEQUENCE public.fishing_grounds_id_seq OWNED BY public.fishing_grounds.id;


--
-- Name: trip_grounds; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.trip_grounds (
    id integer NOT NULL,
    trip_id integer NOT NULL,
    ground_id integer NOT NULL,
    arrival_date timestamp without time zone NOT NULL,
    departure_date timestamp without time zone NOT NULL,
    quality character varying(20)
);


ALTER TABLE public.trip_grounds OWNER TO avtomat_user;

--
-- Name: trip_grounds_id_seq; Type: SEQUENCE; Schema: public; Owner: avtomat_user
--

CREATE SEQUENCE public.trip_grounds_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trip_grounds_id_seq OWNER TO avtomat_user;

--
-- Name: trip_grounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avtomat_user
--

ALTER SEQUENCE public.trip_grounds_id_seq OWNED BY public.trip_grounds.id;


--
-- Name: trips; Type: TABLE; Schema: public; Owner: avtomat_user
--

CREATE TABLE public.trips (
    id integer NOT NULL,
    boat_id integer NOT NULL,
    departure_date timestamp without time zone NOT NULL,
    return_date timestamp without time zone NOT NULL
);


ALTER TABLE public.trips OWNER TO avtomat_user;

--
-- Name: trips_id_seq; Type: SEQUENCE; Schema: public; Owner: avtomat_user
--

CREATE SEQUENCE public.trips_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trips_id_seq OWNER TO avtomat_user;

--
-- Name: trips_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avtomat_user
--

ALTER SEQUENCE public.trips_id_seq OWNED BY public.trips.id;


--
-- Name: boats id; Type: DEFAULT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.boats ALTER COLUMN id SET DEFAULT nextval('public.boats_id_seq'::regclass);


--
-- Name: catches id; Type: DEFAULT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.catches ALTER COLUMN id SET DEFAULT nextval('public.catches_id_seq'::regclass);


--
-- Name: crew_members id; Type: DEFAULT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.crew_members ALTER COLUMN id SET DEFAULT nextval('public.crew_members_id_seq'::regclass);


--
-- Name: fish_species id; Type: DEFAULT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.fish_species ALTER COLUMN id SET DEFAULT nextval('public.fish_species_id_seq'::regclass);


--
-- Name: fishing_grounds id; Type: DEFAULT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.fishing_grounds ALTER COLUMN id SET DEFAULT nextval('public.fishing_grounds_id_seq'::regclass);


--
-- Name: trip_grounds id; Type: DEFAULT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.trip_grounds ALTER COLUMN id SET DEFAULT nextval('public.trip_grounds_id_seq'::regclass);


--
-- Name: trips id; Type: DEFAULT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.trips ALTER COLUMN id SET DEFAULT nextval('public.trips_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.alembic_version (version_num) FROM stdin;
9dc2958b3dbb
\.


--
-- Data for Name: boats; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.boats (id, name, boat_type, displacement, build_date, engine_power, fuel_capacity) FROM stdin;
\.


--
-- Data for Name: catches; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.catches (id, trip_ground_id, fish_species_id, weight) FROM stdin;
\.


--
-- Data for Name: crew_members; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.crew_members (id, trip_id, full_name, address, "position") FROM stdin;
\.


--
-- Data for Name: fish_species; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.fish_species (id, name) FROM stdin;
1	Треска
2	Камбала
3	Сельдь
4	Мойва
5	Пикша
6	Окунь
\.


--
-- Data for Name: fishing_grounds; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.fishing_grounds (id, name, latitude, longitude, depth) FROM stdin;
1	Северная банка	\N	\N	\N
2	Южная банка	\N	\N	\N
3	Восточная отмель	\N	\N	\N
4	Западный склон	\N	\N	\N
\.


--
-- Data for Name: trip_grounds; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.trip_grounds (id, trip_id, ground_id, arrival_date, departure_date, quality) FROM stdin;
\.


--
-- Data for Name: trips; Type: TABLE DATA; Schema: public; Owner: avtomat_user
--

COPY public.trips (id, boat_id, departure_date, return_date) FROM stdin;
\.


--
-- Name: boats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: avtomat_user
--

SELECT pg_catalog.setval('public.boats_id_seq', 1, false);


--
-- Name: catches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: avtomat_user
--

SELECT pg_catalog.setval('public.catches_id_seq', 1, false);


--
-- Name: crew_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: avtomat_user
--

SELECT pg_catalog.setval('public.crew_members_id_seq', 1, false);


--
-- Name: fish_species_id_seq; Type: SEQUENCE SET; Schema: public; Owner: avtomat_user
--

SELECT pg_catalog.setval('public.fish_species_id_seq', 6, true);


--
-- Name: fishing_grounds_id_seq; Type: SEQUENCE SET; Schema: public; Owner: avtomat_user
--

SELECT pg_catalog.setval('public.fishing_grounds_id_seq', 4, true);


--
-- Name: trip_grounds_id_seq; Type: SEQUENCE SET; Schema: public; Owner: avtomat_user
--

SELECT pg_catalog.setval('public.trip_grounds_id_seq', 1, false);


--
-- Name: trips_id_seq; Type: SEQUENCE SET; Schema: public; Owner: avtomat_user
--

SELECT pg_catalog.setval('public.trips_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: boats boats_name_key; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_name_key UNIQUE (name);


--
-- Name: boats boats_pkey; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_pkey PRIMARY KEY (id);


--
-- Name: catches catches_pkey; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.catches
    ADD CONSTRAINT catches_pkey PRIMARY KEY (id);


--
-- Name: crew_members crew_members_pkey; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.crew_members
    ADD CONSTRAINT crew_members_pkey PRIMARY KEY (id);


--
-- Name: fish_species fish_species_name_key; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.fish_species
    ADD CONSTRAINT fish_species_name_key UNIQUE (name);


--
-- Name: fish_species fish_species_pkey; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.fish_species
    ADD CONSTRAINT fish_species_pkey PRIMARY KEY (id);


--
-- Name: fishing_grounds fishing_grounds_name_key; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.fishing_grounds
    ADD CONSTRAINT fishing_grounds_name_key UNIQUE (name);


--
-- Name: fishing_grounds fishing_grounds_pkey; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.fishing_grounds
    ADD CONSTRAINT fishing_grounds_pkey PRIMARY KEY (id);


--
-- Name: trip_grounds trip_grounds_pkey; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.trip_grounds
    ADD CONSTRAINT trip_grounds_pkey PRIMARY KEY (id);


--
-- Name: trips trips_pkey; Type: CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_pkey PRIMARY KEY (id);


--
-- Name: catches catches_fish_species_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.catches
    ADD CONSTRAINT catches_fish_species_id_fkey FOREIGN KEY (fish_species_id) REFERENCES public.fish_species(id);


--
-- Name: catches catches_trip_ground_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.catches
    ADD CONSTRAINT catches_trip_ground_id_fkey FOREIGN KEY (trip_ground_id) REFERENCES public.trip_grounds(id);


--
-- Name: crew_members crew_members_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.crew_members
    ADD CONSTRAINT crew_members_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(id);


--
-- Name: trip_grounds trip_grounds_ground_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.trip_grounds
    ADD CONSTRAINT trip_grounds_ground_id_fkey FOREIGN KEY (ground_id) REFERENCES public.fishing_grounds(id);


--
-- Name: trip_grounds trip_grounds_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.trip_grounds
    ADD CONSTRAINT trip_grounds_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(id);


--
-- Name: trips trips_boat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avtomat_user
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- PostgreSQL database dump complete
--

\unrestrict yMNSJhFkg9QmPxxMWOeicO4reeIGzVMdQVoS4unnhAih3LieyS6a74GTDC6mViC


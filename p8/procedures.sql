CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names TEXT[], p_phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT := 1;
    bad_data TEXT := '';
BEGIN
    IF array_length(p_names, 1) <> array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Names and phones arrays must have same length';
    END IF;

    WHILE i <= array_length(p_names, 1) LOOP

        
        IF p_phones[i] ~ '^[0-9]{7,15}$' THEN
            INSERT INTO phonebook(name, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (phone)
            DO UPDATE SET name = EXCLUDED.name;
        ELSE
            bad_data := bad_data || p_names[i] || ':' || p_phones[i] || '; ';
        END IF;

        i := i + 1;
    END LOOP;

    RAISE NOTICE 'Invalid entries: %', bad_data;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$;
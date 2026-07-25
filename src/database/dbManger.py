from typing import Any

import psycopg2

from src.model.aeroplane import Aeroplane


class DBManager:
    def __init__(
            self,
            db_name: str = "aircraft",
            admin_params: dict[str, Any] | None = None,
            conn_params: dict[str, Any] | None = None,
    ) -> None:
        self.db_name = db_name

        self.admin_params = admin_params or {
            "host": "localhost",
            "dbname": "postgres",
            "user": "daniil",
            "password": "123456",
            "port": 5432,
        }

        self.conn_params = conn_params or {
            "host": "localhost",
            "dbname": self.db_name,
            "user": "daniil",
            "password": "123456",
            "port": 5432,
        }

    def create_database(self) -> None:
        """Создает базу данных, если её нет."""
        conn = psycopg2.connect(**self.admin_params)
        conn.autocommit = True
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (self.db_name,),
                )

                if cur.fetchone() is None:
                    cur.execute(f'CREATE DATABASE "{self.db_name}"')
        finally:
            conn.close()

    def create_tables(self) -> None:
        """Создает таблицу aeroplanes, если её нет."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS aeroplanes (
                        icao24 VARCHAR(6) PRIMARY KEY,
                        callsign VARCHAR(8),
                        country VARCHAR(65),
                        velocity REAL,
                        geo_altitude REAL
                    )
                    """
                )
                cur.execute("""
                        DELETE FROM aeroplanes
                    """)
            conn.commit()

    def add_to_database(self, aeroplane: Aeroplane) -> None:
        """Добавляет один самолет в БД."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO aeroplanes (
                        icao24, callsign, country, velocity, geo_altitude
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (icao24) DO NOTHING
                    """,
                    (
                        aeroplane.icao24,
                        aeroplane.callsign,
                        aeroplane.country,
                        aeroplane.velocity,
                        aeroplane.geo_altitude,
                    ),
                )
            conn.commit()

    def init_database(self, aeroplanes: list[Aeroplane]) -> None:
        """Создает БД, таблицу и заполняет её данными."""
        self.create_database()
        self.create_tables()
        for aeroplane in aeroplanes:
            self.add_to_database(aeroplane)

    def get_countries_and_aeroplanes_count(self) -> dict[str, int]:
        """получает список всех стран и количество самолетов в их воздушных пространствах."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        SELECT country, COUNT(*)
                        FROM aeroplanes
                        GROUP BY country
                        ORDER BY country DESC
                        """)
                rows = cur.fetchall()
                return {country: count for country, count in rows}

    def get_all_aeroplanes(self) -> list[Aeroplane]:
        """получает список всех воздушных судов"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        SELECT icao24, callsign, country, velocity, geo_altitude
                        FROM aeroplanes
                        """)
                rows = cur.fetchall()
        return self._rows_to_list(rows)

    def get_avg_speed(self) -> float:
        """получает среднюю скорость по самолетам"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        SELECT AVG(velocity) 
                        FROM aeroplanes
                        """)
                return cur.fetchone()[0]

    def get_aeroplanes_with_higher_speed(self) -> list[Aeroplane]:
        """получает список всех самолетов, у которых скорость выше средней"""
        avg_speed = self.get_avg_speed()
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        SELECT icao24, callsign, country, velocity, geo_altitude
                        FROM aeroplanes
                        WHERE velocity > (%s)
                        """,
                            (avg_speed,))
                rows = cur.fetchall()
        return self._rows_to_list(rows)

    def get_aeroplanes_with_keyword(self, keyword: str) -> list[Aeroplane]:
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT icao24, callsign, country, velocity, geo_altitude
                    FROM aeroplanes
                    WHERE callsign ILIKE %s
                    """,
                    (f"%{keyword}%",)
                )

                rows = cur.fetchall()
        return self._rows_to_list(rows)

    def _rows_to_list(self, rows) -> list[Aeroplane]:
        result: list[Aeroplane] = []
        for row in rows:
            icao24 = row[0]
            callsign = row[1]
            country = row[2]
            velocity = row[3]
            geo_altitude = row[4]

            aeroplane = Aeroplane(
                icao24,
                callsign,
                country,
                velocity,
                geo_altitude
            )
            result.append(aeroplane)
        return result

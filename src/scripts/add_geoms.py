import sys


import pandas as pd
import geopandas as gpd
import basedosdados as bd
from shapely import wkt

from shapely.geometry import mapping
import json

sys.argv.append(["--max-memory", "8G"])


def get_origins(id_municipio):
    origins = bd.read_sql(
        f"""
        with t as (
            SELECT 
                t1.geometria h3_geometry, 
                st_centroid(t1.geometria) geometry,
                RTRIM(t2.nome) bairro,
                row_number() over (partition by id_grid_h3 order by st_area(st_intersection(t1.geometria, t2.geometry))) larger_area,
                quantidade_pessoas
            FROM `basedosdados.br_ipea_acesso_oportunidades.estatisticas_2019` t1 
            JOIN `datario.dados_mestres.bairro` t2
            ON st_intersects(t1.geometria, t2.geometry)
            WHERE id_municipio = '{id_municipio}'
            AND quantidade_pessoas > 0 )
        select 
        row_number() over() id, * except(larger_area)
        from t
        where larger_area = 1
        """,
        billing_project_id="rj-escritorio-dev",
    )

    origins["geometry"] = origins["geometry"].apply(wkt.loads)
    origins["h3_geometry"] = origins["h3_geometry"].apply(wkt.loads)
    return gpd.GeoDataFrame(origins)


def load_stations(station, con):
    station["name"] = station["bairro"].astype(str)
    station["direct_times_fetched"] = True
    station["longitude_e7"] = station["geometry"].apply(lambda x: int(x.x * 10000000))
    station["latitude_e7"] = station["geometry"].apply(lambda x: int(x.y * 10000000))

    con.execute("DROP TABLE IF EXISTS public.stations CASCADE")

    (
        station[
            ["id", "name", "latitude_e7", "longitude_e7", "direct_times_fetched"]
        ].to_sql(
            "stations",
            con,
            schema="public",
            if_exists="replace",
            index=False,
        )
    )


def load_isochrones(
    origins,
    travel_time_matrix,
    con,
    isotype="normal",
    tempos=[30, 45, 60, 90, 120],
    if_exists="replace",
):
    ttm = pd.merge(
        origins.rename(
            columns={
                "geometry": "centroid_h3",
                "h3_geometry": "geometry",
                "id": "to_id",
            }
        )[["geometry", "to_id"]],
        travel_time_matrix.dropna(),
        left_on="to_id",
        right_on="to_id",
    )

    isos = pd.concat(
        [
            ttm[ttm["travel_time"] <= t].dissolve(["from_id"]).assign(duration=t)
            for t in tempos
        ]
    )
    isos["geometry"] = isos["geometry"].apply(lambda x: json.dumps(mapping(x)))
    isos["type"] = isotype

    isos = isos.reset_index()[["from_id", "geometry", "duration", "type"]].rename(
        columns={"from_id": "station_id"}
    )

    isos[["station_id", "duration", "type", "geometry"]].to_sql(
        "isochrones", con, "public", if_exists, index=False
    )

    return isos

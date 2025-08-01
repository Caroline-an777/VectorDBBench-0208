from typing import Annotated, TypedDict, Unpack

import click
from pydantic import SecretStr

from vectordb_bench.backend.clients import DB
from vectordb_bench.cli.cli import (
    CommonTypedDict,
    HNSWFlavor3,
    IVFFlatTypedDictN,
    cli,
    click_parameter_decorators_from_typed_dict,
    run,
)

DBTYPE = DB.Milvus


class MilvusTypedDict(TypedDict):
    uri: Annotated[
        str,
        click.option("--uri", type=str, help="uri connection string", required=True),
    ]
    user_name: Annotated[
        str | None,
        click.option("--user-name", type=str, help="Db username", required=False),
    ]
    password: Annotated[
        str | None,
        click.option("--password", type=str, help="Db password", required=False),
    ]
    num_shards: Annotated[
        int,
        click.option(
            "--num-shards",
            type=int,
            help="Number of shards",
            required=False,
            default=1,
            show_default=True,
        ),
    ]


class MilvusAutoIndexTypedDict(CommonTypedDict, MilvusTypedDict): ...


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusAutoIndexTypedDict)
def MilvusAutoIndex(**parameters: Unpack[MilvusAutoIndexTypedDict]):
    from .config import AutoIndexConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=AutoIndexConfig(),
        **parameters,
    )


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusAutoIndexTypedDict)
def MilvusFlat(**parameters: Unpack[MilvusAutoIndexTypedDict]):
    from .config import FLATConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=FLATConfig(),
        **parameters,
    )


class MilvusHNSWTypedDict(CommonTypedDict, MilvusTypedDict, HNSWFlavor3): ...


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusHNSWTypedDict)
def MilvusHNSW(**parameters: Unpack[MilvusHNSWTypedDict]):
    from .config import HNSWConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=HNSWConfig(
            M=parameters["m"],
            efConstruction=parameters["ef_construction"],
            ef=parameters["ef_search"],
        ),
        **parameters,
    )


class MilvusRefineTypedDict(TypedDict):
    refine: Annotated[
        bool,
        click.option(
            "--refine",
            type=bool,
            required=True,
            help="Whether refined data is reserved during index building.",
        ),
    ]
    refine_type: Annotated[
        str | None,
        click.option(
            "--refine-type",
            type=click.Choice(["SQ6", "SQ8", "BF16", "FP16", "FP32"], case_sensitive=False),
            help="The data type of the refine index to use. Supported values: SQ6,SQ8,BF16,FP16,FP32",
            required=True,
        ),
    ]
    refine_k: Annotated[
        float,
        click.option(
            "--refine-k",
            type=float,
            help="The magnification factor of refine compared to k.",
            required=True,
        ),
    ]


class MilvusHNSWPQTypedDict(CommonTypedDict, MilvusTypedDict, MilvusHNSWTypedDict, MilvusRefineTypedDict):
    nbits: Annotated[
        int,
        click.option(
            "--nbits",
            type=int,
            required=True,
        ),
    ]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusHNSWPQTypedDict)
def MilvusHNSWPQ(**parameters: Unpack[MilvusHNSWPQTypedDict]):
    from .config import HNSWPQConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=HNSWPQConfig(
            M=parameters["m"],
            efConstruction=parameters["ef_construction"],
            ef=parameters["ef_search"],
            nbits=parameters["nbits"],
            refine=parameters["refine"],
            refine_type=parameters["refine_type"],
            refine_k=parameters["refine_k"],
        ),
        **parameters,
    )


class MilvusHNSWPRQTypedDict(
    CommonTypedDict,
    MilvusTypedDict,
    MilvusHNSWPQTypedDict,
):
    nrq: Annotated[
        int,
        click.option(
            "--nrq",
            type=int,
            help="The number of residual subquantizers.",
            required=True,
        ),
    ]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusHNSWPRQTypedDict)
def MilvusHNSWPRQ(**parameters: Unpack[MilvusHNSWPRQTypedDict]):
    from .config import HNSWPRQConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=HNSWPRQConfig(
            M=parameters["m"],
            efConstruction=parameters["ef_construction"],
            ef=parameters["ef_search"],
            nbits=parameters["nbits"],
            refine=parameters["refine"],
            refine_type=parameters["refine_type"],
            refine_k=parameters["refine_k"],
            nrq=parameters["nrq"],
        ),
        **parameters,
    )


class MilvusHNSWSQTypedDict(CommonTypedDict, MilvusTypedDict, MilvusHNSWTypedDict, MilvusRefineTypedDict):
    sq_type: Annotated[
        str | None,
        click.option(
            "--sq-type",
            type=click.Choice(["SQ6", "SQ8", "BF16", "FP16", "FP32"], case_sensitive=False),
            help="Scalar quantizer type. Supported values: SQ6,SQ8,BF16,FP16,FP32",
            required=True,
        ),
    ]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusHNSWSQTypedDict)
def MilvusHNSWSQ(**parameters: Unpack[MilvusHNSWSQTypedDict]):
    from .config import HNSWSQConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=HNSWSQConfig(
            M=parameters["m"],
            efConstruction=parameters["ef_construction"],
            ef=parameters["ef_search"],
            sq_type=parameters["sq_type"],
            refine=parameters["refine"],
            refine_type=parameters["refine_type"],
            refine_k=parameters["refine_k"],
        ),
        **parameters,
    )


class MilvusIVFFlatTypedDict(CommonTypedDict, MilvusTypedDict, IVFFlatTypedDictN): ...


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusIVFFlatTypedDict)
def MilvusIVFFlat(**parameters: Unpack[MilvusIVFFlatTypedDict]):
    from .config import IVFFlatConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=IVFFlatConfig(
            nlist=parameters["nlist"],
            nprobe=parameters["nprobe"],
        ),
        **parameters,
    )


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusIVFFlatTypedDict)
def MilvusIVFSQ8(**parameters: Unpack[MilvusIVFFlatTypedDict]):
    from .config import IVFSQ8Config, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=IVFSQ8Config(
            nlist=parameters["nlist"],
            nprobe=parameters["nprobe"],
        ),
        **parameters,
    )


class MilvusIVFRABITQTypedDict(CommonTypedDict, MilvusTypedDict, MilvusIVFFlatTypedDict):
    rbq_bits_query: Annotated[
        int,
        click.option(
            "--rbq-bits-query",
            type=int,
            help="The magnification factor of refine compared to k.",
            required=True,
        ),
    ]
    refine: Annotated[
        bool,
        click.option(
            "--refine",
            type=bool,
            required=True,
            help="Whether refined data is reserved during index building.",
        ),
    ]
    refine_type: Annotated[
        str | None,
        click.option(
            "--refine-type",
            type=click.Choice(["SQ6", "SQ8", "BF16", "FP16", "FP32"], case_sensitive=False),
            help="The data type of the refine index to use. Supported values: SQ6,SQ8,BF16,FP16,FP32",
            required=True,
        ),
    ]
    refine_k: Annotated[
        float,
        click.option(
            "--refine-k",
            type=float,
            help="The magnification factor of refine compared to k.",
            required=True,
        ),
    ]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusIVFRABITQTypedDict)
def MilvusIVFRabitQ(**parameters: Unpack[MilvusIVFRABITQTypedDict]):
    from .config import IVFRABITQConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=IVFRABITQConfig(
            nlist=parameters["nlist"],
            nprobe=parameters["nprobe"],
            rbq_bits_query=parameters["rbq_bits_query"],
            refine=parameters["refine"],
            refine_type=parameters["refine_type"],
            refine_k=parameters["refine_k"],
        ),
        **parameters,
    )


class MilvusDISKANNTypedDict(CommonTypedDict, MilvusTypedDict):
    search_list: Annotated[str, click.option("--search-list", type=int, required=True)]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusDISKANNTypedDict)
def MilvusDISKANN(**parameters: Unpack[MilvusDISKANNTypedDict]):
    from .config import DISKANNConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=DISKANNConfig(
            search_list=parameters["search_list"],
        ),
        **parameters,
    )


class MilvusGPUIVFTypedDict(CommonTypedDict, MilvusTypedDict, MilvusIVFFlatTypedDict):
    cache_dataset_on_device: Annotated[
        str,
        click.option("--cache-dataset-on-device", type=str, required=True),
    ]
    refine_ratio: Annotated[str, click.option("--refine-ratio", type=float, required=True)]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusGPUIVFTypedDict)
def MilvusGPUIVFFlat(**parameters: Unpack[MilvusGPUIVFTypedDict]):
    from .config import GPUIVFFlatConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=GPUIVFFlatConfig(
            nlist=parameters["nlist"],
            nprobe=parameters["nprobe"],
            cache_dataset_on_device=parameters["cache_dataset_on_device"],
            refine_ratio=parameters.get("refine_ratio"),
        ),
        **parameters,
    )


class MilvusGPUBruteForceTypedDict(CommonTypedDict, MilvusTypedDict):
    metric_type: Annotated[
        str,
        click.option("--metric-type", type=str, required=True, help="Metric type for brute force search"),
    ]
    limit: Annotated[
        int,
        click.option("--limit", type=int, required=True, help="Top-k limit for search"),
    ]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusGPUBruteForceTypedDict)
def MilvusGPUBruteForce(**parameters: Unpack[MilvusGPUBruteForceTypedDict]):
    from .config import GPUBruteForceConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=GPUBruteForceConfig(
            metric_type=parameters["metric_type"],
            limit=parameters["limit"],  # top-k for search
        ),
        **parameters,
    )


class MilvusGPUIVFPQTypedDict(
    CommonTypedDict,
    MilvusTypedDict,
    MilvusIVFFlatTypedDict,
    MilvusGPUIVFTypedDict,
):
    m: Annotated[str, click.option("--m", type=int, help="hnsw m", required=True)]
    nbits: Annotated[str, click.option("--nbits", type=int, required=True)]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusGPUIVFPQTypedDict)
def MilvusGPUIVFPQ(**parameters: Unpack[MilvusGPUIVFPQTypedDict]):
    from .config import GPUIVFPQConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=GPUIVFPQConfig(
            nlist=parameters["nlist"],
            nprobe=parameters["nprobe"],
            m=parameters["m"],
            nbits=parameters["nbits"],
            cache_dataset_on_device=parameters["cache_dataset_on_device"],
            refine_ratio=parameters["refine_ratio"],
        ),
        **parameters,
    )


class MilvusGPUCAGRATypedDict(CommonTypedDict, MilvusTypedDict, MilvusGPUIVFTypedDict):
    intermediate_graph_degree: Annotated[
        str,
        click.option("--intermediate-graph-degree", type=int, required=True),
    ]
    graph_degree: Annotated[str, click.option("--graph-degree", type=int, required=True)]
    build_algo: Annotated[str, click.option("--build_algo", type=str, required=True)]
    team_size: Annotated[str, click.option("--team-size", type=int, required=True)]
    search_width: Annotated[str, click.option("--search-width", type=int, required=True)]
    itopk_size: Annotated[str, click.option("--itopk-size", type=int, required=True)]
    min_iterations: Annotated[str, click.option("--min-iterations", type=int, required=True)]
    max_iterations: Annotated[str, click.option("--max-iterations", type=int, required=True)]


@cli.command()
@click_parameter_decorators_from_typed_dict(MilvusGPUCAGRATypedDict)
def MilvusGPUCAGRA(**parameters: Unpack[MilvusGPUCAGRATypedDict]):
    from .config import GPUCAGRAConfig, MilvusConfig

    run(
        db=DBTYPE,
        db_config=MilvusConfig(
            db_label=parameters["db_label"],
            uri=SecretStr(parameters["uri"]),
            user=parameters["user_name"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            num_shards=int(parameters["num_shards"]),
        ),
        db_case_config=GPUCAGRAConfig(
            intermediate_graph_degree=parameters["intermediate_graph_degree"],
            graph_degree=parameters["graph_degree"],
            itopk_size=parameters["itopk_size"],
            team_size=parameters["team_size"],
            search_width=parameters["search_width"],
            min_iterations=parameters["min_iterations"],
            max_iterations=parameters["max_iterations"],
            build_algo=parameters["build_algo"],
            cache_dataset_on_device=parameters["cache_dataset_on_device"],
            refine_ratio=parameters["refine_ratio"],
        ),
        **parameters,
    )

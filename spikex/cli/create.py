from pathlib import Path

from srsly import json_dumps
from wasabi import msg

from .. import __version__ as spikex_version
from ..templates.wikigraph import get_meta
from ..wikigraph import WikiGraph


def create_wikigraph(
    wiki="en",
    version="latest",
    output_path: Path = None,
    dumps_path: Path = None,
    max_workers: int = None,
    silent: bool = None,
    force: bool = None,
):
    if not output_path.exists():
        output_path.mkdir()
        msg.good(f"Created output directory: {output_path}")
    graph_name = f"{wiki}wiki_core"
    graph_path = output_path.joinpath(graph_name)
    if not force and graph_path.exists():
        msg.fail(
            f"Output path already contains {graph_name} directory",
            "Use --force to overwrite it",
            exits=1,
        )
    kwargs = {
        "dumps_path": dumps_path,
        "max_workers": max_workers,
        "wiki": wiki,
        "version": version,
        "verbose": not silent,
    }
    wg = WikiGraph.build(**kwargs)
    if not graph_path.exists():
        graph_path.mkdir()
    graph_format = "picklez"
    with msg.loading("dump to disk..."):
        wg.dump(graph_path, graph_format=graph_format)
    meta = get_meta()
    meta["name"] = graph_name
    meta["version"] = wg.version
    meta["graph_format"] = graph_format
    meta["spikex_version"] = f">={spikex_version}"
    meta["fullname"] = f"{graph_name}-{spikex_version}"
    meta["sources"].append("Wikipedia")
    meta_path = graph_path.joinpath("meta.json")
    meta_path.write_text(json_dumps(meta, indent=2))
    msg.good(f"Successfully created {graph_name}.")

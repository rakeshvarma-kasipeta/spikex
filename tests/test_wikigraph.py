import pytest

from respacy.wikigraph import WikiGraph


@pytest.mark.slow()
def test_wikigraph():
    wg = WikiGraph(version="tech_latest")
    print([wg.get_title(vx) for vx in wg.get_path(8254753, 692903)])

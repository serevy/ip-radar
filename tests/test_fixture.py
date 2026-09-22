from ip_radar.fixtures import graph_from_github_fixture


FIXTURE = "evals/readme-i18n-kit/pr-3-8.json"


def test_readme_i18n_fixture_is_frozen_and_loads_as_graph():
    graph = graph_from_github_fixture(FIXTURE)

    assert [item.id for item in graph.timeline()] == [
        "pr-3",
        "pr-4",
        "pr-5",
        "pr-6",
        "pr-7",
        "pr-8",
    ]
    assert len(graph.edges()) == 5
    assert graph.validate_temporal_edges() == ()

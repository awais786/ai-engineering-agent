from __future__ import annotations

from typing import Any, Protocol

from langgraph.graph import END, START, StateGraph

from agentsys.graph.nodes import make_node
from agentsys.graph.state import WorkflowState


class _Agent(Protocol):
    name: str

    async def run(self, state: WorkflowState) -> dict[str, Any]: ...


async def _merge(state: WorkflowState) -> dict[str, Any]:
    errored = any(
        sub.error is not None
        for sub in (state.pm, state.dev, state.reviewer, state.fixer)
    )
    return {"status": "failed" if errored else "completed"}


def build_graph(agents: dict[str, _Agent], *, checkpointer: Any) -> Any:
    graph: StateGraph = StateGraph(WorkflowState)

    graph.add_node("pm", make_node(agents["pm"]))
    graph.add_node("dev", make_node(agents["dev"]))
    graph.add_node("reviewer", make_node(agents["reviewer"]))
    graph.add_node("fixer", make_node(agents["fixer"]))
    graph.add_node("merge", _merge)

    graph.add_edge(START, "pm")
    graph.add_edge("pm", "dev")
    graph.add_edge("dev", "reviewer")
    graph.add_edge("reviewer", "fixer")
    graph.add_edge("fixer", "merge")
    graph.add_edge("merge", END)

    return graph.compile(checkpointer=checkpointer)

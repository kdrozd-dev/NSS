# AGENTS.md

## Purpose

This repo is a small Python prototype for a CDN routing assignment. Keep changes focused on routing logic, comparison metrics, and readable script output.

## Repo Shape

- `nss.py` contains the fixed topology, CDN server list, and routing code.
- `task.txt` contains the assignment details.

## Working Rules

- Keep the topology and server list easy to find and edit.
- Preserve the distinction between `different_servers(...)` and `same_server(...)`.
- Use deterministic, structured outputs so routing variants can be compared.
- Do not mutate the original graph across user evaluations; use graph copies per computation.
- Count a request as rejected only when the required number of node-disjoint routes cannot be produced.
- In this assignment, the ‘naive’ method is the greedy approach that deletes used nodes and uses Dijkstra shortest-path searche

## Scope

- Support `k=2` and `k=3`.
- Compare same-server and different-server routing variants.
- Report average route length in links and request rejection ratio.
- Keep script-level printing simple; make plotting optional.

## Validation

- Use the workspace virtual environment.
- Install dependencies with `pip install networkx matplotlib` if needed.
- Run `python nss.py` from the repository root.

# Building with Claude API

Just some practice code and notes I wrote while going through Anthropic's "Building with the Claude API" course. Nothing polished here, mostly scratch scripts for trying things out (first calls, streaming, tool use, prompt evals, etc.).

Don't expect it to be a clean or complete reference. It's for my own learning.

## Running stuff

Needs an Anthropic API key in a `.env` file:

```
ANTHROPIC_API_KEY=your-key-here
```

Then with [uv](https://docs.astral.sh/uv/):

```bash
uv add anthropic python-dotenv
uv run first_call.py
```

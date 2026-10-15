"""Trust stack: every script is checked by separate agents, then by a fixed-rule gate.

  claims     independent claim extraction (adds claims the writer missed)
  verifier   BLIND re-sourcing: sees claim text only, finds its own sources; code recounts independence
  factcheck  is each claim worded precisely? (may read the verifier's evidence URLs, nothing else)
  bias       tone, framing, balance (script only)
  legal      names, minors, victims, allegations (script and claim flags only)
  gate       deterministic PUBLISH / REWRITE / HOLD / KILL (no model)
  loop       claims -> verifier | bias | legal -> factcheck -> gate, rewriting until a final decision

Each checker is its own call and never sees another checker's verdicts. Import the pieces from their
modules; this package file stays empty on purpose so importing one checker does not load the rest.
"""

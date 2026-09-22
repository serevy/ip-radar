# Sparse-history abstention fixture

This synthetic fixture captures a pattern observed during third-party repository review without copying third-party implementation content into IP Radar.

A detailed change and an unrelated maintenance change may touch the same file. That overlap is useful as a weak relationship signal, but it is not sufficient evidence of shared technical intent, refinement, or candidate lineage.

Expected behavior:

- retain the shared-path signal;
- do not create a semantic edge from that signal alone;
- report `insufficient_evidence` when no stronger evidence is available.

This fixture intentionally tests the ability to **not** grow a lineage.

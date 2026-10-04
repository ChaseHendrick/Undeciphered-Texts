# A two-stream mix, not a four-stream copy

4 October 2026. No letter string is stored.

DeepSeek's mHC widens a residual from one stream to several and projects the mix onto doubly stochastic matrices with Sinkhorn, so a deep stack cannot amplify. A later measurement of DeepSeek-V4-Flash found that a block usually uses about two of the four streams, and that mixing in the later layers is close to the identity.

Bob is two layers deep. Copying four streams would add the part of that result that went unused. `engine.neural_manifold` mixes two streams, runs 20 Sinkhorn steps, and keeps the L1 norm from growing across 32 mixes. A strong diagonal stays the identity, which is the mapping mHC was built to protect.

The mix is not in the format 5 forward pass. The shipped weights were not read and not replaced. A new format would still have to pass the promotion gate. This is not a claim that a two-layer router beats a large language model.

No letter string is stored.

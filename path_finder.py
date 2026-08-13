import typing
from validate_and_build import MazeConfig

"""
ext piece: how a queue mechanically produces the ring order, without you ever labeling "this is ring 1, this is ring 2."

Take a small branching example (not a straight corridor this time):


S connects to A and B   (A, B are 1 move from S)
A connects to C          (C is 2 moves from S)
B connects to D          (D is 2 moves from S)
Exit = D. Rule: add newly-found cells to the back of the queue, always process from the front, mark a cell visited the instant it's added (so it can't be added twice).

Pop	Is it exit?	Newly discovered → added to back	Queue afterward
S	no	A, B	[A, B]
A	no	C	[B, C]
B	no	D	[C, D]
C	no	(nothing new)	[D]
D	yes — stop	—	—
Look at the order things got popped: S, then A, B (both ring 1), then C, D (both ring 2). A and B were both fully processed before C or D was touched — even though D was found (added to the queue) while processing B, one step after C was found while processing A. The queue didn't know or care about "rings" as a concept. It happened automatically, purely from the add-to-back / remove-from-front rule: everything found while processing ring 1 gets queued up behind the rest of ring 1, but ahead of anything ring 2 will later discover.

That's the proof, not an assertion: FIFO order = ring order, for free.

One more detail visible in the trace: notice I said "mark visited the instant it's added," not "when it's processed." If I'd waited, both A and B might try to discover the same ring-2 cell independently before either got marked, and it'd end up in the queue twice. Marking on add prevents that.

Does the "why FIFO order = ring order" proof land? If yes, next is the last piece: came_from, which I'll ground the same concrete way using this exact S/A/B/C/D example instead of abstract "notebook" language.


"""


def find_path(output_file: typing.IO[str], config_obj: MazeConfig) -> None:
    ...

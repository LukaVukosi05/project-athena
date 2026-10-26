# Grade 8 Graphs Lesson 1 — Cartesian coordinates and ordered pairs

**Status:** Original draft for mathematics teacher review. This is source content, not a published interactive lesson. The questions below are newly authored; they are not copies of past papers or Siyavula exercises.

**CAPS scope:** The 2026 Grade 8 annual teaching plan asks learners to use tables or ordered pairs to plot points and draw graphs on a Cartesian plane. This first lesson teaches the coordinate plane, scale, signs, ordered pairs and plotting. Connecting points to draw a relationship is reserved for the next lesson. [Department of Basic Education 2026 Grade 8 ATP](https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208). [Siyavula Grade 8 graph chapter](https://www.siyavula.com/read/za/mathematics/grade-8/graphs/23-graphs-06).

## Lesson contract

- **ID:** `g8-graphs-01`; **topic:** `graphs`; **position:** Topic 4, Lesson 1.
- **Goal:** Read, plot and verify an ordered pair on correctly labelled axes, including zero, negative coordinates, non-unit scales and context units.
- **Prerequisites:** Integers, number lines, tables of values, horizontal and vertical directions.
- **Duration:** Approximately 80 minutes.
- **Why it matters:** A swapped coordinate or an incorrect scale produces a wrong graph even when the table and formula are right.
- **Core idea:** Start at the origin. Move horizontally by the first coordinate, then vertically by the second. Check the axis labels, interval size and original ordered pair before accepting the plotted point.
- **Release gate:** A maths teacher checks all coordinates and context language; all 15 runtime animations, answer gating, practice and reassessment must pass before `release_approved` becomes true.

## Whiteboard behavior shared by every question

The whiteboard receives the *current question's* axes, bounds, tick interval, points, labels and required operation. It never recycles the previous example's plotted coordinates. The initial state shows the full question, axes and only points explicitly given. Targetable SVG objects include `x-axis`, `y-axis`, `origin`, `x-tick-N`, `y-tick-N`, `x-guide`, `y-guide`, `point-N`, `point-label-N`, `operation`, `result` and `verification`. Each step preserves previous plotted points. Operation phase highlights the active axis and draws one guide; result phase plots or names the requested object. Previously completed results remain visible during the next step's ready and operation phases. Next and Previous reconstruct the same scene. Narration and captions say the same words; reduced motion reveals the same objects in the same order.

Use a square grid with mathematically scaled coordinates, not decorative dots. Coordinate values are stored as numbers, never inferred by parsing prose. For a point `(x, y)`, the SVG location is `originX + x * pixelsPerUnitX` and `originY - y * pixelsPerUnitY`. Unit scales may differ across axes and must be labelled. Questions about a single point must not draw an invented continuous line. Questions about a finite set retain separate points unless a later question expressly asks for a connection.

For each example: show problem → locate origin → read x → travel horizontally → read y → travel vertically → plot/identify → read back coordinates → verify. Only steps relevant to the question are active; do not show the target point or final coordinates at initial load.

## Worked example bank

### 01 Foundation — first quadrant point

**Question (2 marks):** On axes marked in ones, plot `A(2, 3)`. Name its x-coordinate and y-coordinate.

**Board:** Axes from −1 to 5; `A` absent initially. Highlight x-axis, move a guide from 0 to 2, then highlight y-axis and grow the vertical guide from `(2, 0)` to `(2, 3)`. Reveal `A` at the intersection, retain both guides until verification. Caption each move.

**Memo:** The first coordinate is 2, so move two units right. The second is 3, so move three units up. Plot `A(2, 3)`. Reading from A back to the axes gives x = 2 and y = 3. **Misconception:** moving up before reading x. **Repair:** trace horizontal move first on a second point `(3, 2)`; compare the different positions.

### 02 Easy — read a point

**Question (2 marks):** Point B is shown three squares right and one square up from the origin. Write B as an ordered pair.

**Board:** B is a given plotted dot, with coordinate text hidden. Draw its vertical projection to x = 3, then horizontal projection to y = 1; reveal `B(3, 1)` only after both have been read. Do not move B while teaching.

**Memo:** Horizontal coordinate 3 comes first; vertical coordinate 1 comes second. B = `(3, 1)`. Check by moving from the origin to the given dot. **Misconception:** writing `(1, 3)`. **Repair:** show both candidate dots simultaneously and point to the one originally supplied.

### 03 Easy — point on the x-axis

**Question (2 marks):** Plot `C(4, 0)` and explain which axis contains C.

**Board:** Travel right four units, show the zero vertical displacement as a short highlighted y-axis label, then plot C on the x-axis. Never animate a move upward.

**Memo:** x = 4 and y = 0. C is `(4, 0)` on the x-axis. Substitute the visible zero back into the ordered pair. **Misconception:** interpreting zero as the origin regardless of the other coordinate. **Repair:** compare `(4, 0)` with `(0, 0)` on the same axes.

### 04 Standard — point on the y-axis

**Question (3 marks):** Point D is five units below the origin on the vertical axis. Give D's coordinates and state why its x-coordinate is zero.

**Board:** Highlight the vertical axis, show no horizontal displacement, then move downward five units and reveal D at `(0, −5)`. Preserve the sign in the label and verification.

**Memo:** No horizontal movement gives x = 0; five units down gives y = −5. D = `(0, −5)`. The x-coordinate is zero because D lies on the y-axis. **Misconception:** writing `(−5, 0)`. **Repair:** project D onto both axes and ask which projection stays at zero.

### 05 Standard — quadrant II

**Question (3 marks):** Plot `E(−3, 2)` on axes marked from −5 to 5. State its quadrant.

**Board:** Show −3 on the left half of the x-axis, guide left by three, then guide up by two; add the Quadrant II highlight *after* E is plotted.

**Memo:** x = −3 means left; y = 2 means up. E is at `(−3, 2)` in Quadrant II. Read back left three and up two. **Misconception:** a negative x implies moving down. **Repair:** color horizontal and vertical signed directions separately.

### 06 Standard — quadrant III

**Question (3 marks):** Plot `F(−2, −4)` and name its quadrant.

**Board:** First move two left to `(−2, 0)`; then move four down to `(−2, −4)`. Label F only at the final location. Highlight the bottom-left region for quadrant recognition.

**Memo:** Both coordinates are negative, so F is left of and below the origin. F lies in Quadrant III. Verify projections −2 and −4. **Misconception:** two minus signs make a positive point. **Repair:** distinguish coordinate directions from multiplying signed numbers.

### 07 Intermediate — quadrant IV and reversed pair

**Question (4 marks):** Plot `G(3, −2)` and `H(−2, 3)`. Explain why G and H are different points.

**Board:** Plot G in two moves and freeze its guides; plot H in two moves using a different accent color. Leave both points visible. Show `G: right 3, down 2` and `H: left 2, up 3` next to their respective dots.

**Memo:** G is `(3, −2)` in Quadrant IV; H is `(−2, 3)` in Quadrant II. They differ because the first coordinate governs horizontal movement and the second vertical movement. **Misconception:** treating an ordered pair as an unordered set. **Repair:** swap the pair and watch the second dot move to another quadrant.

### 08 Intermediate — non-unit scale

**Question (4 marks):** The horizontal ticks read 0, 2, 4, 6, … and vertical ticks read 0, 5, 10, 15, …. Plot `J(6, 10)` and report how many grid intervals you moved on each axis.

**Board:** Bind x ticks to two units and y ticks to five units. Count three horizontal intervals and two vertical intervals; place J only at the intersection. Display the numeric labels throughout.

**Memo:** 6 ÷ 2 = 3 intervals right, and 10 ÷ 5 = 2 intervals up. J is `(6, 10)`. Read the labels, not the number of squares, to verify. **Misconception:** treating each square as one on both axes. **Repair:** label every relevant tick, then compare the dot produced by the incorrect `(3, 2)` interpretation.

### 09 Intermediate — mixed negative scale

**Question (4 marks):** Both axes increase by 2 per grid interval. Plot `K(−4, 6)` and state the quadrant.

**Board:** Count two intervals left to x = −4 and three up to y = 6. Mark K in Quadrant II. Reveal the tick labels before plotting, and retain them during verification.

**Memo:** −4 ÷ 2 gives two intervals left; 6 ÷ 2 gives three intervals up. K is `(−4, 6)` in Quadrant II. **Misconception:** moving four full grid intervals left. **Repair:** annotate the tick sequence 0, −2, −4 before moving.

### 10 Exam — read several plotted points

**Question (5 marks):** A grid shows P at `(−1, 4)`, Q at `(0, −3)` and R at `(4, 0)`, with labels but no coordinates. Write each ordered pair and state which points lie on an axis.

**Board:** The three plotted dots are given; never hide them. Reveal only one pair at a time. For P, show its two projections; repeat for Q and R. Keep the earlier coordinate labels visible as later points are read.

**Memo:** P = `(−1, 4)`; Q = `(0, −3)` is on the y-axis; R = `(4, 0)` is on the x-axis. Verify each against the original dot. **Misconception:** any negative coordinate means the point is not on an axis. **Repair:** compare the coordinate equal to zero for Q and R.

### 11 Exam — identify one erroneous plot

**Question (5 marks):** A learner was asked to plot M at `(−3, 1)` but placed M at `(1, −3)`. Locate the learner's first error and draw the correct point.

**Board:** Show the learner's dot in amber, not as the answer. Highlight the first coordinate `−3` and the learner's incorrect rightward move to 1. Replay from the origin: left three, up one; add corrected M in teal while preserving the original error dot for comparison.

**Memo:** The learner reversed the coordinate roles: `−3` is the x-coordinate, not the y-coordinate. Correct M is `(−3, 1)`. Check by projecting to x = −3 and y = 1. **Misconception:** reversing x and y. **Repair:** rehearse the phrase “across first, then up or down” with `(1, −3)` as a distinct point.

### 12 Exam — context and units

**Question (5 marks):** On a chart, x is time in minutes and y is distance in kilometres. Plot `(4, 6)` and explain its meaning. The horizontal scale is 2 minutes per tick; the vertical scale is 3 km per tick.

**Board:** Label axes and units, count two time intervals right and two distance intervals up, plot the point, then reveal the sentence “After 4 minutes, the distance is 6 km.” Do not connect the point to the origin; no travel path is specified.

**Memo:** `(4, 6)` means 4 minutes and 6 km. Two intervals of 2 minutes give 4; two intervals of 3 km give 6. **Misconception:** swapping units or inventing a constant-speed line. **Repair:** link each coordinate to the corresponding axis title and leave the single observation as a dot.

### 13 Advanced — reflection diagnostic

**Question (6 marks):** Plot A at `(−2, 3)`, then identify B three units directly below A. Give B's coordinates. Explain which coordinate changed.

**Board:** Plot A; hold its x-guide at −2. Animate a vertical movement from y = 3 to y = 0, counting three down. Plot B at `(−2, 0)` and keep A visible. Do not reflect across an axis; this is a translation.

**Memo:** Moving directly down preserves x = −2. Subtract three from the y-coordinate: 3 − 3 = 0. B = `(−2, 0)`. Verify A and B share a vertical line. **Misconception:** subtracting three from both coordinates. **Repair:** lock the horizontal guide while changing only y.

### 14 Advanced — constrained unknown coordinate

**Question (6 marks):** T lies on the y-axis and four units above `(0, −1)`. Write T's ordered pair and verify both conditions.

**Board:** Mark the given point at `(0, −1)`. Hold the x-position at 0, move four vertical units up through the origin to y = 3, reveal T at `(0, 3)`. Show the axis condition and the four-step count separately.

**Memo:** On the y-axis, x = 0. Start at y = −1 and add 4 to get y = 3. Therefore T = `(0, 3)`. It lies on the y-axis and is four units above `(0, −1)`. **Misconception:** calculating −1 − 4 = −5 despite “above”. **Repair:** use a signed vertical number line before plotting.

### 15 Advanced — multi-point error audit

**Question (7 marks):** A learner plots A `(−2, 0)`, B `(0, 2)`, C `(2, −2)` on axes with x ticks one unit apart and y ticks two units apart. They place C two squares right and two squares down. Is C correct? Give the correct grid movement and check A and B.

**Board:** Show learner C in amber at `(2, −4)`; keep A and B as given dots. Reveal the y-axis labels 0, −2, −4. Keep horizontal x = 2 fixed; move C up from the second square below to the first square below, at `(2, −2)`. Project A and B to verify their coordinates and axis membership. Retain erroneous and corrected C dots with distinct labels.

**Memo:** C is incorrect: two x squares right gives x = 2, but each y square represents 2, so two down gives y = −4. Correct C uses two x squares right and one y square down, yielding `(2, −2)`. A is on the x-axis at `(−2, 0)` and B on the y-axis at `(0, 2)`. **Misconception:** using the x-axis interval as the y-axis interval. **Repair:** label both scales and correct C without moving its x-coordinate.

## Independent practice

No answer appears until submission. Each prompt receives two progressive hints: direction/axis first, then scale or projection. After an incorrect attempt, reveal the first wrong coordinate and request a parallel retry.

1. Plot `(1, 4)` on unit axes. **Answer:** one right, four up.
2. Read a point two left and one up. **Answer:** `(−2, 1)`.
3. Plot `(0, −4)` and name its axis. **Answer:** y-axis.
4. Plot `(−5, 0)` and name its axis. **Answer:** x-axis.
5. Plot `(−1, −3)`; identify Quadrant III. **Answer:** one left, three down.
6. Plot `(4, −2)`; identify Quadrant IV. **Answer:** four right, two down.
7. Compare `(2, −1)` and `(−1, 2)` by plotting both. **Answer:** distinct quadrants IV and II.
8. With x ticks of 2 and y ticks of 4, plot `(6, 8)`. **Answer:** three right, two up.
9. With both ticks of 3, plot `(−6, 9)`. **Answer:** two left, three up.
10. A dot sits on x = 0 and y = 5. **Answer:** `(0, 5)`, y-axis.
11. Correct a learner who puts `(−4, 2)` at `(2, −4)`. **Answer:** four left, two up.
12. Time in hours is x and cost in rand is y. Interpret `(3, 45)`. **Answer:** after three hours, cost is R45.
13. From `(1, −2)`, move up three units. **Answer:** `(1, 1)`.
14. From `(−3, 4)`, move right five units. **Answer:** `(2, 4)`.
15. A y-axis scale of 5 per tick places a learner's `(2, 10)` three ticks up. Correct it. **Answer:** x = 2 as given, y = 10 is two ticks up.

## Mastery and parallel reassessment

**Mastery, five questions:** (1) Plot `(−3, 2)` and name quadrant; (2) read a given dot at `(0, −4)` and name axis; (3) use x scale 2/y scale 5 to plot `(4, −10)`; (4) diagnose swapped `(−1, 3)` shown at `(3, −1)`; (5) translate `(−2, −1)` three units up and justify unchanged x. **Answers:** Quadrant II; y-axis; two x intervals right/two y intervals down; correct point one left and three up; `(−2, 2)`. Award marks for separate coordinate directions, scale and checking. Threshold 80%.

**Parallel reassessment, three questions:** (1) Plot `(−4, −1)` and name quadrant III; (2) x ticks 3/y ticks 2, plot `(6, 4)` using two intervals on each axis; (3) from `(0, −3)` move up five to `(0, 2)` and verify y-axis membership. Use a different numeric set after reteaching.

## Implementation cautions

- The example bank is a draft awaiting teacher approval, not an assertion of completed runtime functionality.
- No graph should be inferred from a lesson title. Each question supplies actual bounds, scales, coordinates and which points are given versus derived.
- Do not join dots unless the question asks for a continuous relationship. Avoid silently using equal numeric scales when tick values differ.
- Preserve earlier dots and coordinate labels between steps. The written memo must match the visual at each step.
- Test initial answer hiding, every operation/result transition, Previous/Next and replay, mobile axis labels, no horizontal overflow, and reduced motion.

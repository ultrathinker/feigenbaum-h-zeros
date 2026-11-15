# Appendix C. Informal explanations

This appendix contains no claims of the work and is not relied upon in it. It explains in words what sections 1–5 are about, for a reader who wants to understand the meaning of the construction before analyzing its details.

## C.1. The two constants

If you slowly turn the knob on a simple system with feedback, it first oscillates between two states, then between four, eight, sixteen. The moments at which the number of states doubles come faster and faster, and the ratio of the intervals tends to the same number 4.669… — regardless of which system you are using. This is the first Feigenbaum constant δ.

The second constant α describes not "when" but "by how many times": at each doubling the picture of the orbit near the critical point compresses by about a factor of 2.503. The universality of both is explained by the fact that period doubling is the application of the same operator T to the family of maps itself, and this operator has a fixed point G, to which everything collapses. δ is the rate at which the operator stretches along the unique unstable direction; α sits in the fixed point itself.

## C.2. What is H

Imagine that we look at the orbit through a microscope whose magnification grows together with the level of doubling. The function H compares the picture at adjacent magnifications: the numerator is where the orbit ends up after 2^(m+1) steps, the denominator is where it was after 2^m steps.

Its zeros correspond to events when the orbit returns exactly to the initial point. In the theory of dynamical systems such regimes are called superstable and are considered the most "regular": they lie at the center of each stability window.

Crucially, H is a function of the **complex** parameter. Real zeros correspond to the usual superstable regimes; complex zeros extend the same picture to where the parameter is no longer a physically meaningful number, but where the Mandelbrot set lives. Our work is a rigorous census of these events in the complex plane.

## C.3. Why interval arithmetic is needed

Ordinary computer computations round, and in long chains the error accumulates unpredictably. Interval arithmetic stores an interval instead of a number, guaranteed to contain the true value: if the truth at the input lies inside the interval, then at the output the truth lies inside the output interval, no matter what rounding does.

Intervals grow during computations — sometimes catastrophically — but the statement "the zero lies in this disk" becomes a proof, not an observation.

The growth of intervals has a non-obvious consequence worth mentioning separately. It gives errors **in both directions**. A false refusal ("the orbit has left the domain") is immediately visible and forces one to look for the cause. But an underestimated margin looks like an honest, just less convincing result — and pushes one to weaken the claim where it was not necessary to weaken it. The second is more dangerous than the first precisely because it does not look like an error.

## C.4. Why holomorphy matters

The method of counting zeros looks at how many times the image of a contour winds around the origin. This number of revolutions is easy to compute for a finite level H_m: it is a finite composition, and can be taken in intervals.

But we need the zeros not of H_m, but of the limit H. The transfer of the number of revolutions from H_m to H is elementary in itself and does not require holomorphy: it suffices that on the contour H is closer to H_m than H_m is to zero. But the conversion of the number of revolutions of the limit function into the **number of its zeros inside** already requires that the limit function be smooth in the complex sense — holomorphic.

For finite approximations this is obvious. For the limit it is not, and this is exactly what is proved in section 5.

## C.5. How the holomorphy of the limit was proved

The direct path looks like this: control the orbit of length 2^m as m grows. It does not work: the orbit length doubles with each level, the intervals blow up, and the margin disappears before the convergence becomes visible.

A bypass uses the fact that period doubling is the application of an operator. Instead of tracing the orbit of length 2^k, one can go up the "renormalization tower" by k − 7 steps and apply the same base functional. The length of the chain drops from 2^m to m — from exponential to linear. This is what makes the problem countable.

Next one needs to show that the slices converge as one goes up the tower. Here the structure of the operator works: it has exactly one unstable direction, and the linear part does not generate it — if the component along the unstable direction was zero, it stays zero. The nonlinear part generates it, and the contribution of this generation is estimated by a separate, third term in the final estimate. It was precisely this term that was missed in earlier estimates, and its inclusion reduced the claimed margin by about a factor of two — from 1.87×10⁻⁷ to 0.87×10⁻⁷.

## C.6. What the link with the Mandelbrot set means

The Mandelbrot set near its Feigenbaum point is self-similar with coefficient δ: by enlarging the picture by a factor of 4.669 you see roughly the same thing. This is an established fact, and we do not discover it.

Our contribution is different. Self-similarity says "the pattern repeats", but it does not say **which** pattern. The zeros of the function H are exactly that pattern, written in universal coordinates not tied to any family. The rigorous catalogue of 23 positions turns the qualitative "repeats" into a testable prediction: here are 23 specific points, find near each one the superstable parameter of the quadratic family.

The experiment of section 7 does exactly this: 22 out of 23 find a partner on the first attempt.

This check has a pitfall worth understanding, because we stumbled on it once (section 7.5). Since the picture is self-similar, it has many "floors": at a radius δ times larger lies a copy of the same pattern. If the test does not fix which floor it is searching on, it will be confirmed on any floor — and the result will look convincing, without actually checking anything. What fixes the floor is the exact-period check: at the target floor the period is 2048, at the neighbouring one 1024. Without this check the test is content-free.

steelix
=======

Better python profiling

Next Steps:
 * Display file names better
 * Investigate potential bug: why are no results deeper than 2 layers deep being displayed?
 * Show percentages on left a la New Relic
 * Color coding!

Known Issues:
 * There are occasional cycles that mean that a particular call stack can be expanded out forever. We should probably figure out how to detect and disconnect them.

steelix
=======

Better python profiling

Next Steps:
 * Take in actual command line arguments for the filename
 * Display file names better
 * Fix header and footer
 * Show percentages on left a la New Relic
 * Color coding!

Known Issues:
 * There are occasional cycles that mean that a particular call stack can be expanded out forever. We should probably figure out how to detect and disconnect them.

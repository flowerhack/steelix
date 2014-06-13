steelix
=======

Better python profiling

Next Steps:
 * Fix header and footer
 * Color coding!

Known Issues:
 * The way we get the root node right now is not entirely accurate. We will probably need to do something smarter than ref counting.
 * There are occasional cycles that mean that a particular call stack can be expanded out forever. We should probably figure out how to detect and disconnect them.

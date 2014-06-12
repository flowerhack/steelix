import urwid
import pstats

class StatInfo(object):
    """
    An object that contains profiling stats for one function in one file.

    Attributes:
        filename (str)
        line_number (int)
        function_name (str)

        num_calls (int)
        total_time (float)
        cumulative_time(float)

        children_dictionary:
            A dictionary with key (filename, line_number, function_name) and two types of possible values:
                the 4-tuple (num_calls, num_calls, total_time, cumulative_time)
                    or
                the 5-tuple (num_calls, num_calls, total_time, cumulative_time, children_dictionary).

        key_tuple:
            A 3-tuple (filename, line_number, function_name).
    """
    def __init__(self, key_tuple, value_tuple):
        self.filename = key_tuple[0]
        self.line_number = key_tuple[1]
        self.function_name = key_tuple[2]
        self.num_calls = value_tuple[0]
        self.total_time = value_tuple[2]
        self.cumulative_time = value_tuple[3]
        if len(value_tuple) > 4:
            self.children_dictionary = value_tuple[4]
        else:
            self.children_dictionary = None

        self.key_tuple = key_tuple

class ProfileBrowser(object):
    """ A browser-type object that holds the StatNodes so they can be displayed via urwid. """
    palette = [
        ('body', 'black', 'light gray'),
        ('flagged', 'black', 'dark green', ('bold','underline')),
        ('focus', 'light gray', 'dark blue', 'standout'),
        ('flagged focus', 'yellow', 'dark cyan',
                ('bold','standout','underline')),
        ('head', 'yellow', 'black', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black','underline'),
        ('title', 'white', 'black', 'bold'),
        ('dirmark', 'black', 'dark cyan', 'bold'),
        ('flag', 'dark gray', 'light gray'),
        ('error', 'dark red', 'light gray'),
        ]

    def __init__(self, filename='myprof.profile'):
        self.stats = pstats.Stats(filename).stats
        self.root = StatInfo(
            ('Filename', "Line Number", 'Function'),
            ('Number of Calls','Number of Calls', 'Total Time', 'Cumulative Time', self.stats)
        )
        self.listbox = urwid.TreeListBox(urwid.TreeWalker(StatNode(self.root)))
        self.listbox.offset_rows = 1
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(urwid.Text("lolerskater"), 'head'),
            footer=urwid.Text("roflcopter"))

    def main(self):
        """ Run the program"""
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.unhandled_input)
        self.loop.run()

    def unhandled_input(self, k):
        # update display of focus directory
        if k in ('q','Q'):
            raise urwid.ExitMainLoop()




class StatNode(urwid.ParentNode):
    """ An urwid.ParentNode object used to load information from StatInfo objects and display them. """

    def __init__(self, stat_info, parent=None, depth=0):
        self.key = stat_info.key_tuple
        self.parent = parent
        self.stat_info = stat_info
        self.depth = depth
        urwid.ParentNode.__init__(self, stat_info, key=self.key, parent=parent, depth=depth)

    def load_parent(self):
        return self.parent

    def load_child_keys(self):
        # TODO: Sort children at this point in the flow.
        children = self.stat_info.children_dictionary
        if children:
            # We pull the contents of the child dictionary into a list so we can sort them.
            child_list = []
            for key in children:
                child_list.append(StatInfo(key, children[key]))
            # Sort by total_time in descending order.
            child_list.sort(key=lambda x: x.total_time, reverse=True)
            # Return a list of only the keys.
            return [item.key_tuple for item in child_list]
        else:
            return []

    def load_child_node(self, key):
        if key is None:
            return EmptyNode(None)
        else:
            children = self.stat_info.children_dictionary
            child = StatInfo(key, children[key])
            return StatNode(child, parent=self, depth=self.depth+1)

    def load_widget(self):
        return StatWidget(self)


class StatWidget(urwid.TreeWidget):
    """ Widget for a StatNode object.  Used for things like keypresses, display text, etc """
    def __init__(self, node):
        super(StatWidget, self).__init__(node)
        self.expanded = False
        self.update_expanded_icon()

    def get_display_text(self):
        stat_info = self.get_node().stat_info
        # TODO: Decide what we most want to display here.
        return ' '.join([stat_info.filename, str(stat_info.total_time)])

    def selectable(self):
        return True

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        key = self.__super.keypress(size, key)
        if key:
            key = self.unhandled_keys(size, key)
        return key

    def unhandled_keys(self, size, key):
        """
        Override this method to intercept keystrokes in subclasses.
        Default behavior: Toggle flagged on space, ignore other keys.
        """
        if key == " ":
            self.flagged = not self.flagged
            self.update_w()
        if key == "e":
            #print self.expanded
            self.expanded = not self.expanded
        else:
            return key

    def update_w(self):
        pass

def main():
    ProfileBrowser().main()

if __name__=="__main__":
    main()

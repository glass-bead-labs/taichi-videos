'''static.py - set up static resources for taichi_videos'''

import os
import bowerstatic

bower = bowerstatic.Bower()
# Currently configured to look from directory where run
curr_dir = os.getcwd()
components = bower.components('app',
                              os.path.join(curr_dir, 'bower_components') )

### This stuff is just straight not working... :(

# Local components must still have a bower.json
all_components = bower.local_components('local', components)
all_components.component(os.path.join(curr_dir, 'resources/taichi_style'),
                # Make the "version" change whenever code is changed
                # This should be changed for "production", but we're unlikely to
                # use this code in high-volume situations.
                version=None)

import os
import sys

#from logilab.common.configuration import ConfigurationMixIn

from astroid.manager import AstroidManager

from pylint.pyreverse.inspector import Linker, project_from_files
from pylint.pyreverse.main import Run
from pylint.pyreverse.diadefslib import DiadefsHandler
from pylint.pyreverse.utils import insert_default_options
from pylint.config.configuration_mixin import ConfigurationMixIn
from pylint.config.options_provider_mixin import OptionsProviderMixIn


# TODO: Get package arg and add to PATH as well.

class PyreverseAdapter(Run):
    """Integrate with pyreverse by overriding its CLI Run class to
    create diagram definitions that can be passed to a writer."""

    def __init__(self, args):
        ConfigurationMixIn.__init__(self, usage=__doc__)
        insert_default_options()
        #self.manager = AstroidManager()
        #self.manager.priority = -1
        #self.manager.options = []
        #self.register_options_provider(self.manager)
        self.args = self.load_command_line_configuration()

    def run(self):
        if not self.args:
            print(self.help())
            return
        # Insert current working directory to the python path to recognize
        # dependencies to local modules even if cwd is not in the PYTHONPATH.
        sys.path.insert(0, os.getcwd())
        try:
            project = project_from_files(self.args)
            linker = Linker(project, tag=True)
            handler = DiadefsHandler(self.config)
            diadefs = handler.get_diadefs(project, linker)
        finally:
            sys.path.pop(0)

        return diadefs


def getDiagramDefinitions(args):
    """Entry point from outside."""
    return PyreverseAdapter(args).run()

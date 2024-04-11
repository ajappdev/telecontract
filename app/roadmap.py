# APP DECLARATIONS
import app.models as am

# CLASS DECLARATIONS

class RoadMapProject:
    """
    This class gives the summary of a project roadmap. Here we will find all
    the functions we need to see all the details related to a project versions
    statistics, and actions
    """

    def __init__(
            self,
            project: am.Project,):

        # Declaring class attributes
        self.project = project
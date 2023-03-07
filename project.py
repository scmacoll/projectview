import os
import hou
from PySide2 import QtWidgets, QtUiTools


class ProjectManager(QtWidgets.QWidget):
    def __init__(self):  # constructor`
        super(ProjectManager, self).__init__()

        self.proj = hou.getenv('JOB') + '/'

        # Load UI file
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('/Users/stu/Library/Preferences/houdini/19.5'
                              '/scripts/python/projectview/projectview.ui')

        # get UI elements (designer)
        self.set_proj = self.ui.findChild(QtWidgets.QPushButton, 'setproj')
        self.proj_path = self.ui.findChild(QtWidgets.QLabel, 'projpath')
        self.proj_name = self.ui.findChild(QtWidgets.QLabel, 'projname')
        self.scene_list = self.ui.findChild(QtWidgets.QListWidget, 'scenelist')

        # # Create widgets
        # self.btn = QtWidgets.QPushButton('Click me')
        # self.lbl_title = QtWidgets.QLabel("PROJECT MANAGER")  # label Title
        # self.label = QtWidgets.QLabel(self.proj)  # label files
        # self.list_widget = QtWidgets.QListWidget()  # create list widget

        # create connections (/button functionality)
        self.set_proj.clicked.connect(self.set_project)

        # Create layout (how widgets will be organised)
        main_layout = QtWidgets.QVBoxLayout()  # vertical layout

        main_layout.addWidget(self.ui)

        # # Add widgets to layout
        # main_layout.addWidget(self.lbl_title)  # label (title) outside list
        # main_layout.addWidget(self.label)  # label outside list
        # main_layout.addWidget(self.list_widget)  # visible list
        # main_layout.addWidget(self.btn)

        self.setLayout(main_layout)

    def set_project(self):
        set_job = hou.ui.selectFile(title='Select Project Folder',
                                    file_type=hou.fileType.Directory)
        hou.hscript('setenv JOB=' + set_job)
        self.proj = hou.getenv('JOB') + '/'

        proj_name = set_job.split('/')[-2]
        set_job = os.path.dirname(set_job)  # removes "/" @ end of name
        proj_path = os.path.split(set_job)[0]  # removes project name

        self.proj_name.setText(proj_name)
        self.proj_path.setText(proj_path + '/')

        self.create_interface()


# create function to open subdirectory of selected file in list
    def navigate_subdir(self):
        print("navigating subdirectory")
        selected_item = self.scene_list.currentItem().text()
        self.scene_list.clear()

        for file in os.listdir(self.proj + selected_item):
            if not '.' in file:
                self.scene_list.addItem(file)
                self.scene_list.doubleClicked.connect(self.navigate_subdir)


    def create_interface(self):
        print("creating interface")
        self.scene_list.clear()

        for file in os.listdir(self.proj):
            if not '.' in file:
                self.scene_list.addItem(file)
                self.scene_list.doubleClicked.connect(self.navigate_subdir)


        return self.scene_list

from opendrop.app.ift.analysis.main.component import MainComponent
from opendrop.appfw import Component, View, Presenter, ComponentFactory


class AnalysisComponent(Component):
    pass


@AnalysisComponent.view
class AnalysisView(View):
    def __init__(self, cf: ComponentFactory) -> None:
        main_cmp = cf.create(MainComponent)
        main_cmp.widget.show()


@AnalysisComponent.presenter
class AnalysisPresenter(Presenter):
    pass

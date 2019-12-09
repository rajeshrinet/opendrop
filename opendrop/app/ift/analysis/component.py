from opendrop.appfw import Component, View, Presenter


class AnalysisComponent(Component):
    pass


@AnalysisComponent.view
class AnalysisView(View):
    pass


@AnalysisComponent.presenter
class AnalysisPresenter(Presenter):
    pass

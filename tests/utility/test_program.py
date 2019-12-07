from typing import NewType

from injector import Module, provider, inject, InstanceProvider

from opendrop.utility.program import Program


def test_program_loads_modules():
    class MyModule(Module):
        is_loaded = False

        def configure(self, binder):
            MyModule.is_loaded = True

    class MyProgram(Program):
        modules = [MyModule]

    program = MyProgram()
    program.run()

    assert MyModule.is_loaded


def test_program_provides_dependencies_to_main():
    MyKey = NewType('MyKey', int)

    class MyModule(Module):
        @provider
        def my_key(self) -> MyKey:
            return 123

    class MyProgram(Program):
        modules = [MyModule]

        @inject
        def main(self, my_key: MyKey) -> None:
            assert my_key == 123

    program = MyProgram()
    program.run()


def test_program_run_returns_main_return_value():
    class MyProgram(Program):
        modules = []

        def main(self) -> None:
            return 42

    program = MyProgram()
    return_val = program.run()

    assert return_val == 42


def test_program_run_passes_kwargs_to_main():
    class MyProgram(Program):
        modules = []

        def main(self, **kwargs):
            assert kwargs == {
                'abc': 123,
                'x': 42,
            }

    program = MyProgram()
    program.run(abc=123, x=42)


def test_program_configure():
    MyKey = NewType('MyKey', int)

    class MyProgram(Program):
        modules = []

        def configure(self, binder) -> None:
            binder.bind(interface=MyKey, to=InstanceProvider(66))

        @inject
        def main(self, my_key: MyKey) -> None:
            assert my_key == 66

    program = MyProgram()
    program.run()

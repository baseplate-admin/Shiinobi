import typer
from shiinobi.builder.staff import StaffBuilder


def main(name: str):
    x = StaffBuilder().build_dictionary()
    print(x)


if __name__ == "__main__":
    typer.run(main)

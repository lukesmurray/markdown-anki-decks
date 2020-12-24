import typer


def print_error(msg: str):
    typer.secho(
        msg,
        fg=typer.colors.RED,
        err=True,
    )


def print_success(msg: str):
    typer.secho(
        msg,
        fg=typer.colors.GREEN,
    )

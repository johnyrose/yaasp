import functools
import datetime
import traceback

import typer


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            typer.echo(typer.style(error_message, fg=typer.colors.RED, bold=True))

            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            error_log_filename = f"error_{current_time}.log"

            with open(error_log_filename, "w") as error_log:
                error_log.write(f"Error: {str(e)}\n")
                traceback.print_exc(file=error_log)

            typer.echo(f"Error details have been saved to: {error_log_filename}")

    return wrapper

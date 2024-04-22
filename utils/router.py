import importlib.util
import logging
import os
import re

from sanic import Sanic

allowed_methods = (
    "get", "post", "put", "delete", "options", "head", "patch", "trace", "ws")


def convert_to_url_params(input_string: str):
    """
    Convert placeholders in the given string from the format `$variable` to `{variable}`
    for FastAPI route compatibility.
    """
    pattern = r'\$([a-zA-Z0-9_]+)'
    result = re.sub(pattern, r'<\1>', input_string)
    return result


def load_routes(app: Sanic, path: str):
    """
    Load Python modules as route handlers from a specified directory into the FastAPI app.
    This includes handling files at the root of the directory for base ('/') routes.
    """
    logging.info(f"Trying to load routes from {path}...")

    for root, dirs, files in os.walk(path, followlinks=False):
        is_base_directory = (root == path)
        if is_base_directory:
            # Handle files directly in the base path as root handlers
            for file_name in files:
                if file_name.endswith('.py') and file_name[:-3] in allowed_methods:
                    method = file_name[:-3]
                    module_file_path = os.path.join(root, file_name)
                    load_route(app, module_file_path, method, "/")

        # Handle subdirectories
        for found_dir in dirs:
            entry_point = os.path.join(root, found_dir)
            route_path = os.path.relpath(entry_point, start=path).replace("\\", "/")

            for method in allowed_methods:
                module_file_path = os.path.join(entry_point, f"{method}.py")
                if os.path.exists(module_file_path):
                    load_route(
                        app=app,
                        module_file_path=module_file_path,
                        method=method,
                        route_path=route_path
                    )


def load_route(
        app: Sanic,
        module_file_path: str,
        method: str,
        route_path: str
):
    """
    Load a single route handler from a Python file and add it to the given router.
    """

    spec = importlib.util.spec_from_file_location("module_name", module_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    api_route_path = f"/{convert_to_url_params(route_path).strip('/')}"

    if method == "ws":
        app.add_websocket_route(
            uri=api_route_path,
            handler=module.handler,
        )
    else:
        logging.info(
            f"Adding {method.upper()} {api_route_path if api_route_path != '/' else 'root (/)'}")
        logging.info(f"Loading {module_file_path}")

        meta = getattr(module, 'meta', {})

        if meta:
            logging.info(f"Adding meta data: {meta}")

        app.add_route(
            name=api_route_path,
            uri=api_route_path,
            handler=module.handler,
            methods=[method.upper()],
        )

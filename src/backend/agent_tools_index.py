from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel


class ToolSchema(BaseModel):
    name: str
    description: str
    method: str
    url: str
    input_schema: Any
    output_schema: Any


class ToolIndexResponse(BaseModel):
    tools: list[ToolSchema]


def get_json_schema(operation: Mapping[str, Any], section: str) -> Any:
    if section == "input":
        return (
            operation.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema", {})
        )

    for response in operation.get("responses", {}).values():
        schema = (
            response.get("content", {})
            .get("application/json", {})
            .get("schema", {})
        )
        if schema:
            return schema
    return {}


def resolve_openapi_schema(schema: Any, openapi: Mapping[str, Any]) -> Any:
    if not isinstance(schema, dict):
        return schema

    if "$ref" in schema:
        ref_path = schema["$ref"].lstrip("#/").split("/")
        resolved: Any = openapi
        for key in ref_path:
            if not isinstance(resolved, Mapping):
                return schema
            resolved = resolved.get(key)
        return resolve_openapi_schema(resolved, openapi)

    if "allOf" in schema:
        merged: dict[str, Any] = {}
        for part in schema["allOf"]:
            resolved_part = resolve_openapi_schema(part, openapi)
            if isinstance(resolved_part, dict):
                merged.update(resolved_part)
        for key, value in schema.items():
            if key != "allOf":
                merged[key] = resolve_openapi_schema(value, openapi)
        return merged

    if "oneOf" in schema:
        return resolve_openapi_schema(schema["oneOf"][0], openapi) if schema["oneOf"] else {}

    if "anyOf" in schema:
        return resolve_openapi_schema(schema["anyOf"][0], openapi) if schema["anyOf"] else {}

    resolved_schema: dict[str, Any] = {}
    for key, value in schema.items():
        if key == "properties" and isinstance(value, dict):
            resolved_schema[key] = {
                prop_name: resolve_openapi_schema(prop_schema, openapi)
                for prop_name, prop_schema in value.items()
            }
        elif key == "items":
            resolved_schema[key] = resolve_openapi_schema(value, openapi)
        elif key == "additionalProperties" and isinstance(value, dict):
            resolved_schema[key] = resolve_openapi_schema(value, openapi)
        else:
            resolved_schema[key] = value
    return resolved_schema


def materialize_agent_schema(schema: Any, openapi: Mapping[str, Any]) -> Any:
    resolved = resolve_openapi_schema(schema, openapi)

    if not isinstance(resolved, dict):
        return resolved

    schema_type = resolved.get("type")
    if schema_type == "object":
        properties = resolved.get("properties", {})
        return {
            key: materialize_agent_schema(value, openapi)
            for key, value in properties.items()
        }

    if schema_type == "array":
        items = resolved.get("items", {})
        return [materialize_agent_schema(items, openapi)]

    if "properties" in resolved:
        return {
            key: materialize_agent_schema(value, openapi)
            for key, value in resolved["properties"].items()
        }

    if "items" in resolved:
        return [materialize_agent_schema(resolved["items"], openapi)]

    if "enum" in resolved:
        enum_values = resolved["enum"]
        return enum_values[0] if enum_values else None

    if schema_type == "integer":
        return 0
    if schema_type == "number":
        return 0
    if schema_type == "boolean":
        return False
    if schema_type == "string":
        return ""

    return resolved


def build_agent_tool(
    operation: Mapping[str, Any],
    method: str,
    path: str,
    openapi: Mapping[str, Any],
) -> ToolSchema:
    return ToolSchema(
        name=operation.get("operationId", ""),
        description=operation.get("description") or operation.get("summary", ""),
        method=method.upper(),
        url=path,
        input_schema=materialize_agent_schema(get_json_schema(operation, "input"), openapi),
        output_schema=materialize_agent_schema(get_json_schema(operation, "output"), openapi),
    )


def build_tool_index(openapi: Mapping[str, Any]) -> ToolIndexResponse:
    agent_tools: list[ToolSchema] = []

    for path, path_item in openapi.get("paths", {}).items():
        for method, operation in path_item.items():
            agent_tools.append(build_agent_tool(operation, method, path, openapi))

    return ToolIndexResponse(tools=agent_tools)

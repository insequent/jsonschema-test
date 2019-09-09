#!/usr/bin/env python3
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from jsonschema_test.validator import validate_schema, ValidateWithDefaults


class Template(BaseModel):
    name: str
    schema: str


class Product(BaseModel):
    name: str
    config: str


app = FastAPI()

# Intentionally making this difficult to be more db-like
templates: List(Template) = []
products: List(Product) = []


@app.post("/templates")
async def create_template(template: Template) -> Template:
    if [t for t in templates if t.name == template.name]:
        raise Exception("Template already exists!")

    if not validate_schema(template.schema):
        raise Exception("Template schema is not a valid JSON schema")

    templates.append(template)
    return template


@app.get("/templates/{name}")
async def get_template(name: str) -> Template:
    try:
        template = [t for t in templates if t.name == name].pop()
    except AttributeError:
        raise Exception(f"A template with name '{name}' does not exist.")

    return template


@app.post("/products")
async def create_product(name: str, template: str, **kwargs) -> Product:
    if [p for p in products if p.name == name]:
        raise Exception("Product already exists!")

    try:
        template = [t for t in templates if t.name == name].pop()
    except AttributeError:
        raise Exception(f"A template with name '{template}' does not exist.")

    ValidateWithDefaults(template.schema).validate(kwargs)

    product = Product(
        name=name,
        config=kwargs
    )

    return product


@app.get("/products/{name}")
async def get_product(name: str) -> Product:
    try:
        product = [p for p in products if p.name == name].pop()
    except AttributeError:
        raise Exception(f"A product with name '{name}' does not exist")

    return product

import os
from typing import Union

from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from pydantic import BaseModel

from src.utils import redirection_links, logger

app = FastAPI()
shortener_prefix = os.environ['SHORTENER_PREFIX']


class AddParams(BaseModel):
    source_url: Union[str, None] = None


@app.post("/add")
async def add(add_params: AddParams):
    logger.info('Page id %s', add_params.source_url)
    shorten_name = redirection_links.generate_link(add_params.source_url)
    shorten_url = f'{shortener_prefix}{shorten_name}'
    return {'shorten_url': shorten_url}


@app.get("/explore")
def redirect_to_link():
    links_html = "<h2>List of Links:</h2><ul>"
    for link_name, link_url in redirection_links.list().items():
        links_html += f"<li><a href='{link_url}'>{link_name}</a></li>"
    links_html += "</ul>"

    # Return the HTML response
    return HTMLResponse(content=links_html)


@app.get("/{short_link_name}")
def redirect_to_link(short_link_name: str):
    origin_link_name = redirection_links.get_origin_link(short_link_name)
    if origin_link_name is not None:
        return RedirectResponse(url=origin_link_name, status_code=302)
    else:
        raise HTTPException(status_code=404, detail="Link not found")

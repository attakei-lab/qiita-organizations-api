"""HTTP endpoint."""
from pathlib import Path
import httpx
from bs4 import BeautifulSoup, Tag
from fastapi import APIRouter

from . import models


QIITA_URL_BASE = "https://qiita.com/organizations"

router = APIRouter()


@router.get("/", response_model=models.ResourceSet[models.Organization])
async def list_organizations(p: int = 1):
    """Response list of registered organizations."""
    def _parse_element(elm: Tag) -> models.Organization:
        id_ = Path(elm["href"]).name
        h2 = elm.find("h2", {"class": "organizationName"})
        p = h2.next_sibling
        return models.Organization(id=id_, name=h2.text, description=p.text)

    body = models.ResourceSet[models.Organization](data=[])

    resp = httpx.get(f"{QIITA_URL_BASE}?page={p}")
    soup = BeautifulSoup(resp.text, "lxml")
    items = soup.find("div", {"data-test-organization-item-list": "true"})
    if items.next_sibling.name == "div":
        lis = items.next_sibling.find_all("li")
        page_text = lis[1].span
        pagination = models.Pagination(
            pages=page_text.contents[-1],
            current=page_text.contents[0],
        )
        if lis[0].a:
            pagination.prev = f"?p={pagination.current - 1}"
        if lis[2].a:
            pagination.next = f"?p={pagination.current + 1}"

        body.pagination = pagination

    body.data = [_parse_element(item) for item in items.find_all("a")]
    return body

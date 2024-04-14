from typing import TypedDict, Optional


class AccountInfo(TypedDict):
    name: str
    email: str
    title: Optional[str]
    edited_name: Optional[str]
    password: str
    date_or_birth: str
    receive_newsletters: Optional[bool]
    receive_offers: Optional[bool]
    first_name: str
    last_name: str
    company: Optional[str]
    address1: str
    address2: Optional[str]
    country: str
    state: str
    city: str
    zipcode: str
    mobile_number: str

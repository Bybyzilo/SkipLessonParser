from __future__ import annotations
from typing import Any, List

from pydantic import BaseModel


class Payment(BaseModel):
    name: str
    type: int
    overpayment: int
    debt: int
    lastPayment: int
    lastPaymentDate: Any


class Contract(BaseModel):
    contractID: int
    number: str
    date: str
    type: int
    payments: List[Payment]


class Data(BaseModel):
    contracts: List[Contract]
    allowPay: bool
    payOnlyBeta: bool


class PaymentModel(BaseModel):
    data: Data
    state: int
    msg: str
    time: int

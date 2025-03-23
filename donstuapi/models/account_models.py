from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel


class Group(BaseModel):
    item1: str
    item2: int | float


class Plan(BaseModel):
    item1: str
    item2: int | float
    item3: bool


class Kaf(BaseModel):
    kafID: int | float
    kafName: str
    aud: str
    phone: str


class Facul(BaseModel):
    faculID: int | float
    faculName: str
    aud: str
    phone: str


class Data(BaseModel):
    studentID: int | float
    fullName: str
    showZachBook: bool
    domintoryNumber: str
    numberRoom: str
    fullNameT: str
    name: str
    middleName: str
    migrRegistrationAddressProduction: Any
    migrRegistrationDateToMigration: str
    migrRegistrationDateToStudyVisa: str
    isAgreementPersonalData: bool
    agreementProcessingPersonalData: Any
    agreementTransferPersonalData: Any
    numRecordBook: str
    numberMobile: str
    surname: str
    birthday: str
    nationality: str
    group: Group
    email: str
    login: str
    emailForTeams: Any
    admissionYear: str
    lastEnterDate: str
    course: str
    faculty: str
    plan: Plan
    trainingDirection: str
    photoLink: str
    verPhoto: Any
    activeSwapPhotoAndVerification: bool
    activeMigrationRegistration: bool
    isMigrStud: bool
    scientificDirector: Any
    allowChangePass: bool
    showRaspButton: bool
    linkRaspButton: Any
    showGraphButton: bool
    showVedButton: bool
    maxFileSize: str
    showResultButton: bool
    isLocked: bool
    isLockedVed: Any
    libraryСard: Any
    online: bool
    hideLinks: bool
    message: str
    htmlBlock: str
    activeSwapPhoto: bool
    byPassSheets: List
    status: int | float
    ratingActivation: bool
    linkPsychology: str
    portfolioIncluded: bool
    debtsGraphIncluded: bool
    needDormitory: bool
    vkID: int | float
    googleID: Any
    yandexID: Any
    telegramID: Any
    allowChangePassStudent: bool
    hidePlan: bool
    hideMoveStory: bool
    eliteEducationID: Any
    scopusID: Any
    isDstu: bool
    kaf: Kaf
    facul: Facul


class BenchmarkItem(BaseModel):
    _percent: int | float
    text: str
    date: str
    time: float


class AccountInfoModel(BaseModel):
    data: Data
    state: int | float
    msg: str
    benchmark: List[BenchmarkItem]
    time: float

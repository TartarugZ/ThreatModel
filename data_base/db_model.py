from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from typing import Optional


class Base(DeclarativeBase):
    pass


class ThreatBase(Base):
    __tablename__ = "Threat"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column()
    internal_offender: Mapped[int] = mapped_column()
    external_offender: Mapped[int] = mapped_column()
    confidentiality: Mapped[bool] = mapped_column()
    integrity: Mapped[bool] = mapped_column()
    availability: Mapped[bool] = mapped_column()


class DeviceTypeBase(Base):
    __tablename__ = "DeviceType"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300))
    description: Mapped[Optional[str]] = mapped_column()
    # has_threat = relationship("DeviceTypeThreat", back_populates="DeviceTypeBase")


class DeviceTypeThreatBase(Base):
    __tablename__ = "DeviceTypeThreat"
    threat_id: Mapped[int] = mapped_column(ForeignKey("Threat.id"), primary_key=True)
    device_type_id: Mapped[int] = mapped_column(ForeignKey("DeviceType.id"), primary_key=True)
    # to_threat = relationship("Threat", back_populates="DeviceTypeThreatBase")
    # to_device = relationship("DeviceType", back_populates="DeviceTypeThreatBase")


class NegativeResultBase(Base):
    __tablename__ = "NegativeResult"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    damage_type: Mapped[Optional[int]] = mapped_column(default=0)
    description: Mapped[Optional[str]] = mapped_column()


class RealizationWayBase(Base):
    __tablename__ = "RealizationWay"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()


class VulnerabilityBase(Base):
    __tablename__ = "Vulnerability"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(14), unique=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


class VulnerabilitySoftwareBase(Base):
    __tablename__ = "VulnerabilitySoftware"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())


class VulnerabilityTypeBase(Base):
    __tablename__ = "VulnerabilityType"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class VulnerabilitySoftwareTypeBase(Base):
    __tablename__ = "SoftwareTypeVulnerability"
    vulnerability_id: Mapped[int] = mapped_column(ForeignKey("Vulnerability.id"), primary_key=True)
    software_type_id: Mapped[int] = mapped_column(ForeignKey("VulnerabilitySoftware.id"), primary_key=True)


class VulnerabilityTypeVulnerabilityBase(Base):
    __tablename__ = "VulnerabilityTypeVulnerability"
    vulnerability_id: Mapped[int] = mapped_column(ForeignKey("Vulnerability.id"), primary_key=True)
    vulnerability_type_id: Mapped[int] = mapped_column(ForeignKey("VulnerabilityType.id"), primary_key=True)


class TacticBase(Base):
    __tablename__ = "Tactic"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()


class TechniqueBase(Base):
    __tablename__ = "Technique"
    id: Mapped[int] = mapped_column(primary_key=True)
    technique_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    tactic_id: Mapped[int] = mapped_column(ForeignKey("Tactic.id"))
    description: Mapped[Optional[str]] = mapped_column()


class DeviceBase(Base):
    __tablename__ = "Device"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[Optional[str]] = mapped_column(ForeignKey("DeviceType.id"))
    description: Mapped[Optional[str]] = mapped_column()


class DeviceScenarioBase(Base):
    __tablename__ = "DeviceScenario"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"))
    technique_id: Mapped[int] = mapped_column(ForeignKey("Technique.id"))
    threat_id: Mapped[int] = mapped_column(ForeignKey("Threat.id"))
    description: Mapped[Optional[str]] = mapped_column()


class DeviceVulnerabilityBase(Base):
    __tablename__ = "DeviceVulnerability"
    device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"), primary_key=True)
    vulnerability_id: Mapped[int] = mapped_column(ForeignKey("Vulnerability.id"), primary_key=True)


class DeviceThreatBase(Base):
    __tablename__ = "DeviceThreat"
    device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"), primary_key=True)
    threat_id: Mapped[int] = mapped_column(ForeignKey("Threat.id"), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column()


class DeviceNegativeResultBase(Base):
    __tablename__ = "DeviceNegativeResult"
    device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"), primary_key=True)
    negative_result_id: Mapped[int] = mapped_column(ForeignKey("NegativeResult.id"), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column()


class DeviceRealizationBase(Base):
    __tablename__ = "DeviceRealization"
    device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"), primary_key=True)
    realization_way_id: Mapped[int] = mapped_column(ForeignKey("RealizationWay.id"), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column()


class DeviceConnectionBase(Base):
    __tablename__ = "DeviceConnection"
    first_device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"), primary_key=True)
    second_device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column()


class DeviceIpBase(Base):
    __tablename__ = "DeviceIp"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"))
    ip_address: Mapped[str] = mapped_column()


class WorkerBase(Base):
    __tablename__ = "Worker"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    patronymic: Mapped[Optional[str]] = mapped_column(String(53))
    description: Mapped[Optional[str]] = mapped_column()
    insider_result: Mapped[Optional[float]] = mapped_column()


class InsiderCriteriaBase(Base):
    __tablename__ = "InsiderCriteria"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    coefficient: Mapped[int] = mapped_column()


class WorkerInsiderCriteriaBase(Base):
    __tablename__ = "WorkerInsiderCriteria"
    worker_id: Mapped[int] = mapped_column(ForeignKey("Worker.id"), primary_key=True)
    insider_criteria_id: Mapped[int] = mapped_column(ForeignKey("InsiderCriteria.id"), primary_key=True)
    value: Mapped[int] = mapped_column(default=1)


class InsiderCriteriaTypeBase(Base):
    __tablename__ = "InsiderCriteriaType"
    insider_criteria_id:  Mapped[int] = mapped_column(ForeignKey("InsiderCriteria.id"), primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    value: Mapped[float] = mapped_column()


class UserBase(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    role: Mapped[int] = mapped_column()


class OrganizationBase(Base):
    __tablename__ = "Organization"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class OrganizationResponsibilityBase(Base):
    __tablename__ = "OrganizationResponsibility"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    patronymic: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()


class IntruderBase(Base):
    __tablename__ = "Intruder"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    place: Mapped[int] = mapped_column()
    capabilities: Mapped[int] = mapped_column()
    aims: Mapped[str] = mapped_column()
    status: Mapped[int] = mapped_column()
    status_reason: Mapped[Optional[str]] = mapped_column()


class DeviceTypeIntruderBase(Base):
    __tablename__ = "DeviceTypeIntruder"
    intruder_id: Mapped[int] = mapped_column(ForeignKey("Intruder.id"), primary_key=True)
    device_type_id: Mapped[int] = mapped_column(ForeignKey("DeviceType.id"), primary_key=True)


class ImpactTypeBase(Base):
    __tablename__ = "ImpactType"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class DeviceImpactTypeBase(Base):
    __tablename__ = "DeviceImpactType"
    device_id: Mapped[int] = mapped_column(ForeignKey("Device.id"), primary_key=True)
    impact_type_id: Mapped[int] = mapped_column(ForeignKey("ImpactType.id"), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column()


class InterfaceBase(Base):
    __tablename__ = "Interface"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class DeviceTypeInterfaceBase(Base):
    __tablename__ = "DeviceTypeInterface"
    interface_id: Mapped[int] = mapped_column(ForeignKey("Interface.id"), primary_key=True)
    device_type_id: Mapped[int] = mapped_column(ForeignKey("DeviceType.id"), primary_key=True)


class InterfaceRealizationWayBase(Base):
    __tablename__ = "InterfaceRealizationWay"
    interface_id: Mapped[int] = mapped_column(ForeignKey("Interface.id"), primary_key=True)
    realization_way_id: Mapped[int] = mapped_column(ForeignKey("RealizationWay.id"), primary_key=True)


def create_db(engine):
    Base.metadata.create_all(engine)

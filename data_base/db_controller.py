from data_base import db_model
from sqlalchemy.orm import Session
from sqlalchemy import select, func


def get_all_device_type(engine):
    with Session(engine) as session:
        statement = select(db_model.DeviceTypeBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_user_role(engine, username):
    with Session(engine) as session:
        statement = select(db_model.UserBase).where(db_model.UserBase.login == username)
        db_object = session.scalars(statement).one()
        return db_object


def get_ip(engine, device_id):
    with Session(engine) as session:
        statement = select(db_model.DeviceIpBase).where(db_model.DeviceIpBase.device_id == device_id)
        db_object = session.scalars(statement).all()
        return db_object


def delete_threat_device_type(engine, threat_id, device_type_id):
    with Session(engine) as session:
        try:
            statement = select(db_model.DeviceTypeThreatBase).where(
                db_model.DeviceTypeThreatBase.threat_id == threat_id).where(
                db_model.DeviceTypeThreatBase.device_type_id == device_type_id)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_worker_insider_criteria_by_id(engine, number):
    with Session(engine) as session:
        try:
            statement = select(db_model.WorkerInsiderCriteriaBase).where(
                db_model.WorkerInsiderCriteriaBase.insider_criteria_id == number)
            db_object = session.scalars(statement).all()
            for i in db_object:
                session.delete(i)
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_some_by_parameter(engine, obj, parameter, number):
    with Session(engine) as session:
        try:
            statement = select(obj).where(parameter == number)
            db_object = session.scalars(statement).all()
            for i in db_object:
                session.delete(i)
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_negative_by_id(engine, number):
    with Session(engine) as session:
        try:
            statement = select(db_model.NegativeResultBase).where(
                db_model.NegativeResultBase.id == number)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_obj_type_by_id(engine, number):
    with Session(engine) as session:
        try:
            statement = select(db_model.DeviceTypeBase).where(
                db_model.DeviceTypeBase.id == number)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_interface_obj_type_by_id(engine, device_type_id, interface_id):
    with Session(engine) as session:
        try:
            statement = select(db_model.DeviceTypeInterfaceBase).where(
                db_model.DeviceTypeInterfaceBase.device_type_id == device_type_id).where(
                db_model.DeviceTypeInterfaceBase.interface_id == interface_id)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_interface_realization_way_by_id(engine, realization_way_id, interface_id):
    with Session(engine) as session:
        try:
            statement = select(db_model.InterfaceRealizationWayBase).where(
                db_model.InterfaceRealizationWayBase.realization_way_id == realization_way_id).where(
                db_model.InterfaceRealizationWayBase.interface_id == interface_id)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_realization_way_by_id(engine, realization_way_id):
    with Session(engine) as session:
        try:
            statement = select(db_model.RealizationWayBase).where(
                db_model.RealizationWayBase.id == realization_way_id)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_interface_by_id(engine, interface_id):
    with Session(engine) as session:
        try:
            statement = select(db_model.InterfaceBase).where(
                db_model.InterfaceBase.id == interface_id)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def get_interfaces_by_device_type_id(engine, number):
    with Session(engine) as session:
        statement = select(db_model.InterfaceBase).select_from(db_model.DeviceTypeBase).where(
            db_model.DeviceTypeBase.id == number).join(db_model.DeviceTypeInterfaceBase,
                                                       db_model.DeviceTypeInterfaceBase.device_type_id == db_model.DeviceTypeBase.id).join(
            db_model.InterfaceBase, db_model.InterfaceBase.id == db_model.DeviceTypeInterfaceBase.interface_id)
        db_object = session.scalars(statement).all()
        return db_object


def get_object_type_by_ubi_id(engine, number):
    with Session(engine) as session:
        statement = select(db_model.DeviceTypeBase).select_from(db_model.ThreatBase).where(
            db_model.ThreatBase.id == number).join(db_model.DeviceTypeThreatBase,
                                                   db_model.DeviceTypeThreatBase.threat_id == db_model.ThreatBase.id).join(
            db_model.DeviceTypeBase, db_model.DeviceTypeBase.id == db_model.DeviceTypeThreatBase.device_type_id)
        db_object = session.scalars(statement).all()
        return db_object


def get_all_ubi(engine):
    with Session(engine) as session:
        statement = select(db_model.ThreatBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_all_interfaces(engine):
    with Session(engine) as session:
        statement = select(db_model.InterfaceBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_all_some(engine, obj):
    with Session(engine) as session:
        statement = select(obj)
        db_object = session.scalars(statement).all()
        return db_object


def get_worker_insider_by_type_id(engine, insider_criteria_id, insider_criteria_type_id):
    with Session(engine) as session:
        statement = select(db_model.WorkerInsiderCriteriaBase).where(
            db_model.WorkerInsiderCriteriaBase.insider_criteria_id == insider_criteria_id).where(
            db_model.WorkerInsiderCriteriaBase.value == insider_criteria_type_id)
        db_object = session.scalars(statement).all()
        return db_object


def get_impact_types_by_dev_id(engine, device_id):
    with Session(engine) as session:
        statement = select(db_model.ImpactTypeBase.id, db_model.ImpactTypeBase.name).select_from(
            db_model.DeviceBase).where(
            db_model.DeviceBase.id == device_id).join(db_model.DeviceImpactTypeBase,
                                                      db_model.DeviceImpactTypeBase.device_id == db_model.DeviceBase.id).join(
            db_model.ImpactTypeBase, db_model.DeviceImpactTypeBase.impact_type_id == db_model.ImpactTypeBase.id)
        db_object = session.execute(statement)
        return db_object


def get_ubi_by_dev_id(engine, device_id):
    with Session(engine) as session:
        statement = select(db_model.ThreatBase.id, db_model.ThreatBase.name, db_model.ThreatBase.description,
                           db_model.ThreatBase.internal_offender, db_model.ThreatBase.external_offender,
                           db_model.ThreatBase.confidentiality, db_model.ThreatBase.integrity,
                           db_model.ThreatBase.availability).select_from(db_model.DeviceBase).where(
            db_model.DeviceBase.id == device_id).join(db_model.DeviceThreatBase,
                                                      db_model.DeviceThreatBase.device_id == db_model.DeviceBase.id).join(
            db_model.ThreatBase, db_model.DeviceThreatBase.threat_id == db_model.ThreatBase.id)
        db_object = session.execute(statement)
        return db_object


def get_negative_by_dev_id(engine, device_id):
    with Session(engine) as session:
        statement = select(db_model.NegativeResultBase.id, db_model.NegativeResultBase.damage_type,
                           db_model.NegativeResultBase.description).select_from(
            db_model.DeviceBase).where(
            db_model.DeviceBase.id == device_id).join(db_model.DeviceNegativeResultBase,
                                                      db_model.DeviceNegativeResultBase.device_id == db_model.DeviceBase.id).join(
            db_model.NegativeResultBase,
            db_model.DeviceNegativeResultBase.negative_result_id == db_model.NegativeResultBase.id)
        db_object = session.execute(statement)
        return db_object


def get_realization_by_dev_id(engine, device_id):
    with Session(engine) as session:
        statement = select(db_model.RealizationWayBase.id, db_model.RealizationWayBase.name,
                           db_model.RealizationWayBase.description).select_from(
            db_model.DeviceBase).where(
            db_model.DeviceBase.id == device_id).join(db_model.DeviceRealizationBase,
                                                      db_model.DeviceRealizationBase.device_id == db_model.DeviceBase.id).join(
            db_model.RealizationWayBase,
            db_model.DeviceRealizationBase.realization_way_id == db_model.RealizationWayBase.id)
        db_object = session.execute(statement)
        return db_object


def get_vul_by_dev_id(engine, device_id):
    with Session(engine) as session:
        statement = select(db_model.VulnerabilityBase.id, db_model.VulnerabilityBase.code,
                           db_model.VulnerabilityBase.name, db_model.VulnerabilityBase.description).select_from(
            db_model.DeviceBase).where(
            db_model.DeviceBase.id == device_id).join(db_model.DeviceVulnerabilityBase,
                                                      db_model.DeviceVulnerabilityBase.device_id == db_model.DeviceBase.id).join(
            db_model.VulnerabilityBase,
            db_model.DeviceVulnerabilityBase.vulnerability_id == db_model.VulnerabilityBase.id)
        db_object = session.execute(statement)
        return db_object


def get_scenario_by_dev_id_threat_id(engine, device_id, threat_id):
    with Session(engine) as session:
        statement = select(db_model.DeviceScenarioBase.id, db_model.DeviceScenarioBase.device_id,
                           db_model.DeviceScenarioBase.technique_id, db_model.DeviceScenarioBase.threat_id,
                           db_model.DeviceScenarioBase.description, db_model.TechniqueBase.name, db_model.TechniqueBase.tactic_id, db_model.TechniqueBase.technique_id).where(
            db_model.DeviceScenarioBase.device_id == device_id).where(
            db_model.DeviceScenarioBase.threat_id == threat_id).join(db_model.TechniqueBase, db_model.TechniqueBase.id == db_model.DeviceScenarioBase.technique_id)
        db_object = session.execute(statement)
        return db_object


def get_some_by_id(engine, obj, number):
    with Session(engine) as session:
        statement = select(obj).where(obj.id == number)
        db_object = session.scalars(statement).one()
        return db_object


def delete_some_by_id(engine, obj, number):
    with Session(engine) as session:
        try:
            statement = select(obj).where(obj.id == number)
            session.delete(session.scalars(statement).one())
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_worker_criteria_by_id(engine, number):
    with Session(engine) as session:
        try:
            statement = select(db_model.WorkerInsiderCriteriaBase).where(
                db_model.WorkerInsiderCriteriaBase.worker_id == number)
            result = session.scalars(statement).all()
            for i in result:
                session.delete(i)
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_device_connection(engine, first_id, second_id):
    with Session(engine) as session:
        try:
            statement = select(db_model.DeviceConnectionBase).where(
                db_model.DeviceConnectionBase.first_device_id == first_id).where(
                db_model.DeviceConnectionBase.second_device_id == second_id)
            db_object = session.scalars(statement).one()
            if type(db_object) is db_model.DeviceConnectionBase:
                session.delete(db_object)
            else:
                statement = select(db_model.DeviceConnectionBase).where(
                    db_model.DeviceConnectionBase.first_device_id == second_id).where(
                    db_model.DeviceConnectionBase.second_device_id == first_id)
                db_object = session.scalars(statement).one()
                session.delete(db_object)
        except:
            session.rollback()
        else:
            session.commit()


def delete_insider_criteria_type(engine, insider_criteria_id, insider_criteria_type_id):
    with Session(engine) as session:
        try:
            statement = select(db_model.InsiderCriteriaTypeBase).where(
                db_model.InsiderCriteriaTypeBase.insider_criteria_id == insider_criteria_id).where(
                db_model.InsiderCriteriaTypeBase.id == insider_criteria_type_id)
            db_object = session.scalars(statement).one()
            session.delete(db_object)
        except:
            session.rollback()
        else:
            session.commit()


def get_connected_devices_by_id(engine, number):
    try:
        with Session(engine) as session:
            statement = select(db_model.DeviceConnectionBase).where(
                db_model.DeviceConnectionBase.first_device_id == number)
            db_object = session.scalars(statement).all()
            statement = select(db_model.DeviceConnectionBase).where(
                db_model.DeviceConnectionBase.second_device_id == number)
            db_object2 = session.scalars(statement).all()
            device_id = []
            for i in db_object:
                device_id.append(i.second_device_id)
            for i in db_object2:
                device_id.append(i.first_device_id)
            device_id = list(set(device_id))
            devices = []
            for i in device_id:
                statement = select(db_model.DeviceBase).where(
                    db_model.DeviceBase.id == i)
                db_object = session.scalars(statement).one()
                devices.append(db_object)
            print('Bd')
            return devices
    except Exception as e:
        print(e)


def update_some_by_id(engine, obj):
    with Session(engine) as session:
        try:
            session.merge(obj)
        except:
            session.rollback()
            raise
        else:
            session.commit()


def get_all_devices(engine):
    with Session(engine) as session:
        statement = select(db_model.DeviceBase)
        db_object = session.scalars(statement).all()
        return db_object


def vulnerability_search(engine, string):
    try:
        with Session(engine) as session:
            statement = select(db_model.VulnerabilityBase).where(db_model.VulnerabilityBase.code.contains(string))
            db_object1 = session.scalars(statement).all()
            statement = select(db_model.VulnerabilityBase).where(db_model.VulnerabilityBase.name.contains(string))
            db_object2 = session.scalars(statement).all()
            statement = select(db_model.VulnerabilityBase).where(
                db_model.VulnerabilityBase.description.contains(string))
            db_object3 = session.scalars(statement).all()
            db_object = []
            for i in db_object1:
                db_object.append(i)
            for i in db_object2:
                db_object.append(i)
            for i in db_object3:
                db_object.append(i)
            db_object = list(set(db_object))
            return db_object
    except Exception as e:
        print(e)


def count_vulnerabilities(engine):
    with Session(engine) as session:
        length = session.scalar(select(func.count()).select_from(db_model.VulnerabilityBase))
        return length


def get_vulnerabilities(engine, limit, page):
    with Session(engine) as session:
        offset = (page - 1) * limit
        stmt = select(db_model.VulnerabilityBase).limit(limit).offset(offset)
        db_object = session.execute(stmt).scalars().all()
        return db_object


def get_vulnerability_type_by_vul_id(engine, number):
    with Session(engine) as session:
        statement = select(db_model.VulnerabilityTypeBase).select_from(db_model.VulnerabilityBase).where(
            db_model.VulnerabilityBase.id == number).join(db_model.VulnerabilityTypeVulnerabilityBase,
                                                          db_model.VulnerabilityTypeVulnerabilityBase.vulnerability_id == db_model.VulnerabilityBase.id).join(
            db_model.VulnerabilityTypeBase,
            db_model.VulnerabilityTypeVulnerabilityBase.vulnerability_type_id == db_model.VulnerabilityTypeBase.id)
        db_object = session.scalars(statement).all()
        return db_object


def get_vulnerability_software_by_vul_id(engine, number):
    with Session(engine) as session:
        statement = select(db_model.VulnerabilitySoftwareBase).select_from(db_model.VulnerabilityBase).where(
            db_model.VulnerabilityBase.id == number).join(db_model.VulnerabilitySoftwareTypeBase,
                                                          db_model.VulnerabilitySoftwareTypeBase.vulnerability_id == db_model.VulnerabilityBase.id).join(
            db_model.VulnerabilitySoftwareBase,
            db_model.VulnerabilitySoftwareTypeBase.software_type_id == db_model.VulnerabilitySoftwareBase.id)
        db_object = session.scalars(statement).all()
        return db_object


def get_realization_by_interface_id(engine, number):
    with Session(engine) as session:
        statement = select(db_model.RealizationWayBase).select_from(db_model.InterfaceBase).where(
            db_model.InterfaceBase.id == number).join(db_model.InterfaceRealizationWayBase,
                                                      db_model.InterfaceRealizationWayBase.interface_id == db_model.InterfaceBase.id).join(
            db_model.RealizationWayBase,
            db_model.RealizationWayBase.id == db_model.InterfaceRealizationWayBase.realization_way_id)
        db_object = session.scalars(statement).all()
        return db_object


def get_technique_by_tac_id(engine, number):
    with Session(engine) as session:
        statement = select(db_model.TechniqueBase).where(
            db_model.TechniqueBase.tactic_id == number)
        db_object = session.scalars(statement).all()
        return db_object


def get_all_impact_types(engine):
    with Session(engine) as session:
        statement = select(db_model.ImpactTypeBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_insider_criteria_type_by_ins_id(engine, number):
    with Session(engine) as session:
        statement = select(db_model.InsiderCriteriaTypeBase).where(
            db_model.InsiderCriteriaTypeBase.insider_criteria_id == number)
        db_object = session.scalars(statement).all()
        return db_object


def get_all_realization_ways(engine):
    with Session(engine) as session:
        statement = select(db_model.RealizationWayBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_all_negatives(engine):
    with Session(engine) as session:
        statement = select(db_model.NegativeResultBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_threat(engine, code):
    with Session(engine) as session:
        statement = select(db_model.ThreatBase).where(db_model.ThreatBase.id == code)
        db_object = session.scalars(statement).one()
        return db_object


def get_negative_object_impact(engine):
    with Session(engine) as session:
        statement = select(db_model.NegativeResultBase.name, db_model.DeviceTypeBase.name,
                           db_model.ImpactTypeBase.id).select_from(db_model.DeviceBase).join(
            db_model.DeviceNegativeResultBase,
            db_model.DeviceBase.id == db_model.DeviceNegativeResultBase.device_id).join(db_model.NegativeResultBase,
                                                                                        db_model.DeviceNegativeResultBase.negative_result_id == db_model.NegativeResultBase.id).join(
            db_model.DeviceTypeBase, db_model.DeviceBase.type_id == db_model.DeviceTypeBase.id).join(
            db_model.DeviceImpactTypeBase, db_model.DeviceBase.id == db_model.DeviceImpactTypeBase.device_id).join(
            db_model.ImpactTypeBase, db_model.DeviceImpactTypeBase.impact_type_id == db_model.ImpactTypeBase.id)
        result = session.execute(statement)
        return result


def get_worker_criteria(engine, number):
    with Session(engine) as session:
        statement = select(db_model.InsiderCriteriaBase.name, db_model.InsiderCriteriaBase.coefficient,
                           db_model.WorkerInsiderCriteriaBase.value, db_model.WorkerInsiderCriteriaBase.worker_id,
                           db_model.WorkerInsiderCriteriaBase.insider_criteria_id, db_model.InsiderCriteriaTypeBase.id,
                           db_model.InsiderCriteriaTypeBase.name,
                           db_model.InsiderCriteriaTypeBase.value).select_from(
            db_model.WorkerBase).where(
            db_model.WorkerBase.id == number).join(
            db_model.WorkerInsiderCriteriaBase,
            db_model.WorkerInsiderCriteriaBase.worker_id == db_model.WorkerBase.id).join(
            db_model.InsiderCriteriaBase,
            db_model.InsiderCriteriaBase.id == db_model.WorkerInsiderCriteriaBase.insider_criteria_id).join(
            db_model.InsiderCriteriaTypeBase,
            db_model.WorkerInsiderCriteriaBase.insider_criteria_id == db_model.InsiderCriteriaTypeBase.insider_criteria_id).where(
            db_model.InsiderCriteriaTypeBase.id == db_model.WorkerInsiderCriteriaBase.value)
        result = session.execute(statement)
        return result


def get_criteria_type(engine, worker_id, insider_criteria_id):
    with Session(engine) as session:
        statement = select(db_model.InsiderCriteriaTypeBase.id, db_model.InsiderCriteriaTypeBase.name,
                           db_model.InsiderCriteriaTypeBase.value).select_from(
            db_model.WorkerInsiderCriteriaBase).where(
            db_model.WorkerInsiderCriteriaBase.worker_id == worker_id).where(
            db_model.WorkerInsiderCriteriaBase.insider_criteria_id == insider_criteria_id).join(
            db_model.InsiderCriteriaBase,
            db_model.InsiderCriteriaBase.id == db_model.WorkerInsiderCriteriaBase.insider_criteria_id).join(
            db_model.InsiderCriteriaTypeBase,
            db_model.InsiderCriteriaTypeBase.insider_criteria_id == insider_criteria_id)
        result = session.execute(statement)
        return result


def get_object_realization(engine):
    with Session(engine) as session:
        statement = select(db_model.DeviceTypeBase.name, db_model.RealizationWayBase.id).select_from(
            db_model.DeviceBase).join(db_model.DeviceTypeBase,
                                      db_model.DeviceBase.type_id == db_model.DeviceTypeBase.id).join(
            db_model.DeviceRealizationBase, db_model.DeviceBase.id == db_model.DeviceRealizationBase.device_id).join(
            db_model.RealizationWayBase,
            db_model.DeviceRealizationBase.realization_way_id == db_model.RealizationWayBase.id)
        result = session.execute(statement)
        return result


def get_object_interface_realization(engine):
    with Session(engine) as session:
        statement = select(db_model.DeviceTypeBase.name, db_model.InterfaceBase.name,
                           db_model.RealizationWayBase.id).select_from(
            db_model.DeviceBase).join(db_model.DeviceTypeBase,
                                      db_model.DeviceBase.type_id == db_model.DeviceTypeBase.id).join(
            db_model.DeviceTypeInterfaceBase,
            db_model.DeviceTypeInterfaceBase.device_type_id == db_model.DeviceTypeBase.id).join(db_model.InterfaceBase,
                                                                                                db_model.InterfaceBase.id == db_model.DeviceTypeInterfaceBase.interface_id).join(
            db_model.InterfaceRealizationWayBase,
            db_model.InterfaceBase.id == db_model.InterfaceRealizationWayBase.interface_id).join(
            db_model.RealizationWayBase,
            db_model.InterfaceRealizationWayBase.realization_way_id == db_model.RealizationWayBase.id)
        result = session.execute(statement)
        return result


def get_used_ubi(engine):
    with Session(engine) as session:
        statement = select(db_model.ThreatBase.id, db_model.ThreatBase.name, db_model.ThreatBase.internal_offender,
                           db_model.ThreatBase.external_offender).select_from(
            db_model.ThreatBase).join(db_model.DeviceThreatBase,
                                      db_model.DeviceThreatBase.threat_id == db_model.ThreatBase.id)
        result = session.execute(statement)
        return result


def get_negative_by_ubi_id(number, engine):
    with Session(engine) as session:
        statement = select(db_model.NegativeResultBase.id).select_from(db_model.ThreatBase).where(
            db_model.ThreatBase.id == number).join(db_model.DeviceThreatBase,
                                                   db_model.ThreatBase.id == db_model.DeviceThreatBase.threat_id).join(
            db_model.DeviceBase, db_model.DeviceBase.id == db_model.DeviceThreatBase.device_id).join(
            db_model.DeviceNegativeResultBase,
            db_model.DeviceNegativeResultBase.device_id == db_model.DeviceBase.id).join(db_model.NegativeResultBase,
                                                                                        db_model.NegativeResultBase.id == db_model.DeviceNegativeResultBase.negative_result_id)
        result = session.execute(statement)
        return result


def get_obj_by_ubi_id(number, engine):
    with Session(engine) as session:
        statement = select(db_model.DeviceTypeBase.name).select_from(db_model.ThreatBase).where(
            db_model.ThreatBase.id == number).join(db_model.DeviceThreatBase,
                                                   db_model.ThreatBase.id == db_model.DeviceThreatBase.threat_id).join(
            db_model.DeviceBase, db_model.DeviceBase.id == db_model.DeviceThreatBase.device_id).join(
            db_model.DeviceTypeBase, db_model.DeviceTypeBase.id == db_model.DeviceBase.type_id)
        result = session.execute(statement)
        return result


def get_realization_by_ubi_id(number, engine):
    with Session(engine) as session:
        statement = select(db_model.RealizationWayBase.id).select_from(db_model.ThreatBase).where(
            db_model.ThreatBase.id == number).join(db_model.DeviceThreatBase,
                                                   db_model.ThreatBase.id == db_model.DeviceThreatBase.threat_id).join(
            db_model.DeviceBase, db_model.DeviceBase.id == db_model.DeviceThreatBase.device_id).join(
            db_model.DeviceRealizationBase, db_model.DeviceRealizationBase.device_id == db_model.DeviceBase.id).join(
            db_model.RealizationWayBase,
            db_model.RealizationWayBase.id == db_model.DeviceRealizationBase.realization_way_id)
        result = session.execute(statement)
        return result


def get_scenario_by_ubi_id(number, engine):
    with Session(engine) as session:
        statement = select(db_model.DeviceScenarioBase.device_id, db_model.TechniqueBase.tactic_id,
                           db_model.TechniqueBase.technique_id).select_from(db_model.DeviceScenarioBase).where(
            db_model.DeviceScenarioBase.threat_id == number).join(db_model.TechniqueBase,
                                                                  db_model.TechniqueBase.id == db_model.DeviceScenarioBase.technique_id)
        result = session.execute(statement)
        return result


def get_all_software_type(engine):
    with Session(engine) as session:
        statement = select(db_model.VulnerabilitySoftwareBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_all_vulnerabilities_type(engine):
    with Session(engine) as session:
        statement = select(db_model.VulnerabilityTypeBase)
        db_object = session.scalars(statement).all()
        return db_object


def get_vulnerability_by_code(engine, code):
    with Session(engine) as session:
        statement = select(db_model.VulnerabilityBase).where(db_model.VulnerabilityBase.code == code)
        db_object = session.scalars(statement).one()
        return db_object


def create_some(some, engine):
    with Session(engine) as session:
        try:
            session.add(some)
        except:
            session.rollback()
            raise
        else:
            session.commit()

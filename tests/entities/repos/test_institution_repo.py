import pytest
from regtech_api_commons.models.auth import AuthenticatedUser
from regtech_user_fi_management.entities.models.dao import (
    AddressStateDao,
    FederalRegulatorDao,
    HMDAInstitutionTypeDao,
    SBLInstitutionTypeDao,
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    SblTypeMappingDao,
    LeiStatusDao,
)
from regtech_cleanup_api.entities.repos import institution_repo as repo
from sqlalchemy.orm import Session, scoped_session


class TestInstitutionsRepo:
    auth_user: AuthenticatedUser = AuthenticatedUser.from_claim({"id": "test_user_id"})

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, transaction_session: Session, session_generator: scoped_session):
        state_ga, state_ca, state_fl = (
            AddressStateDao(code="GA", name="Georgia"),
            AddressStateDao(code="CA", name="California"),
            AddressStateDao(code="FL", name="Florida"),
        )
        transaction_session.add(state_ga)
        transaction_session.add(state_ca)
        transaction_session.add(state_fl)

        fr_dao_fri1, fr_dao_fri2, fr_dao_fri3 = (
            FederalRegulatorDao(id="FRI1", name="Test Federal Regulator ID 1"),
            FederalRegulatorDao(id="FRI2", name="Test Federal Regulator ID 2"),
            FederalRegulatorDao(id="FRI3", name="Test Federal Regulator ID 3"),
        )
        transaction_session.add(fr_dao_fri1)
        transaction_session.add(fr_dao_fri2)
        transaction_session.add(fr_dao_fri3)

        hmda_it_dao_hit1, hmda_it_dao_hit2, hmda_it_dao_hit3 = (
            HMDAInstitutionTypeDao(id="HIT1", name="Test HMDA Instituion ID 1"),
            HMDAInstitutionTypeDao(id="HIT2", name="Test HMDA Instituion ID 2"),
            HMDAInstitutionTypeDao(id="HIT3", name="Test HMDA Instituion ID 3"),
        )
        transaction_session.add(hmda_it_dao_hit1)
        transaction_session.add(hmda_it_dao_hit2)
        transaction_session.add(hmda_it_dao_hit3)

        sbl_it_dao_sit1, sbl_it_dao_sit2, sbl_it_dao_sit3 = (
            SBLInstitutionTypeDao(id="1", name="Test SBL Instituion ID 1"),
            SBLInstitutionTypeDao(id="2", name="Test SBL Instituion ID 2"),
            SBLInstitutionTypeDao(id="13", name="Test SBL Instituion ID Other"),
        )
        transaction_session.add(sbl_it_dao_sit1)
        transaction_session.add(sbl_it_dao_sit2)
        transaction_session.add(sbl_it_dao_sit3)

        fi_dao_123, fi_dao_456, fi_dao_sub_456 = (
            FinancialInstitutionDao(
                name="Test Bank 123",
                lei="TESTBANK123000000000",
                lei_status_code="ISSUED",
                lei_status=LeiStatusDao(code="ISSUED", name="Issued", can_file=True),
                domains=[FinancialInstitutionDomainDao(domain="test.bank.1", lei="TESTBANK123000000000")],
                tax_id="12-3456789",
                rssd_id=1234,
                primary_federal_regulator_id="FRI1",
                hmda_institution_type_id="HIT1",
                sbl_institution_types=[SblTypeMappingDao(sbl_type=sbl_it_dao_sit1, modified_by="test_user_id")],
                hq_address_street_1="Test Address Street 1",
                hq_address_street_2="",
                hq_address_street_3="",
                hq_address_street_4="",
                hq_address_city="Test City 1",
                hq_address_state_code="GA",
                hq_address_zip="00000",
                parent_lei="012PARENTTESTBANK123",
                parent_legal_name="PARENT TEST BANK 123",
                parent_rssd_id=12345,
                top_holder_lei="01234TOPHOLDERLEI123",
                top_holder_legal_name="TOP HOLDER LEI 123",
                top_holder_rssd_id=123456,
                modified_by="test_user_id",
            ),
            FinancialInstitutionDao(
                name="Test Bank 456",
                lei="TESTBANK456000000000",
                lei_status_code="RETIRED",
                lei_status=LeiStatusDao(code="RETIRED", name="Retired", can_file=False),
                domains=[FinancialInstitutionDomainDao(domain="test.bank.2", lei="TESTBANK456000000000")],
                tax_id="98-7654321",
                rssd_id=4321,
                primary_federal_regulator_id="FRI2",
                hmda_institution_type_id="HIT2",
                sbl_institution_types=[SblTypeMappingDao(sbl_type=sbl_it_dao_sit2, modified_by="test_user_id")],
                hq_address_street_1="Test Address Street 2",
                hq_address_street_2="",
                hq_address_street_3="",
                hq_address_street_4="",
                hq_address_city="Test City 2",
                hq_address_state_code="CA",
                hq_address_zip="11111",
                parent_lei="012PARENTTESTBANK456",
                parent_legal_name="PARENT TEST BANK 456",
                parent_rssd_id=54321,
                top_holder_lei="01234TOPHOLDERLEI456",
                top_holder_legal_name="TOP HOLDER LEI 456",
                top_holder_rssd_id=654321,
                modified_by="test_user_id",
            ),
            FinancialInstitutionDao(
                name="Test Sub Bank 456",
                lei="TESTSUBBANK456000000",
                lei_status_code="LAPSED",
                lei_status=LeiStatusDao(code="LAPSED", name="Lapsed", can_file=False),
                domains=[FinancialInstitutionDomainDao(domain="sub.test.bank.2", lei="TESTSUBBANK456000000")],
                tax_id="76-5432198",
                rssd_id=2134,
                primary_federal_regulator_id="FRI3",
                hmda_institution_type_id="HIT3",
                sbl_institution_types=[
                    SblTypeMappingDao(sbl_type=sbl_it_dao_sit3, modified_by="test_user_id", details="test")
                ],
                hq_address_street_1="Test Address Street 3",
                hq_address_street_2="",
                hq_address_street_3="",
                hq_address_street_4="",
                hq_address_city="Test City 3",
                hq_address_state_code="FL",
                hq_address_zip="11111",
                parent_lei="012PARENTTESTBANK456",
                parent_legal_name="PARENT TEST SUB BANK 456",
                parent_rssd_id=21435,
                top_holder_lei="01234TOPHOLDERLEI456",
                top_holder_legal_name="TOP HOLDER LEI SUB BANK 456",
                top_holder_rssd_id=321654,
                modified_by="test_user_id",
            ),
        )

        transaction_session.add(fi_dao_123)
        transaction_session.add(fi_dao_456)
        transaction_session.add(fi_dao_sub_456)

        transaction_session.commit()

    def test_delete_domains_by_lei(self, transaction_session: Session, query_session: Session):
        repo.delete_domains_by_lei(transaction_session, "TESTBANK123000000000")
        res = query_session.query(FinancialInstitutionDomainDao).all()
        res_leis = [fininst.lei for fininst in res]
        assert "TESTBANK123000000000" not in res_leis
        assert "TESTBANK456000000000" in res_leis
        assert "TESTSUBBANK456000000" in res_leis

    def test_delete_sbl_type_by_lei(self, transaction_session: Session, query_session: Session):
        repo.delete_sbl_type_by_lei(transaction_session, "TESTBANK123000000000")
        res = query_session.query(SblTypeMappingDao).all()
        res_types = [t.sbl_type.name for t in res]
        assert "Test SBL Instituion ID 1" not in res_types
        assert "Test SBL Instituion ID 2" in res_types
        assert "Test SBL Instituion ID Other" in res_types

    def test_delete_institution(self, transaction_session: Session, query_session: Session):
        repo.delete_institution(transaction_session, "TESTBANK123000000000")
        res = query_session.query(FinancialInstitutionDao).all()
        res_institution_names = [n.name for n in res]
        assert "Test Bank 123" not in res_institution_names
        assert "Test Bank 456" in res_institution_names
        assert "Test Sub Bank 456" in res_institution_names

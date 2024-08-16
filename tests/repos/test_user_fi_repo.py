import pytest
from regtech_cleanup_api.entities.repos import user_fi_repo as repo
from regtech_user_fi_management.entities.repos import institutions_repo
from regtech_api_commons.models.auth import AuthenticatedUser
from sqlalchemy.orm import Session
from regtech_user_fi_management.entities.models.dao import (
    SBLInstitutionTypeDao,
    FinancialInstitutionDao,
    SblTypeMappingDao,
    FinancialInstitutionDomainDao,
)


class TestInstitutionsRepo:
    auth_user: AuthenticatedUser = AuthenticatedUser.from_claim({"id": "test_user_id"})

    @pytest.fixture(scope="function", autouse=True)
    def setup(
        self,
        transaction_session: Session,
    ):

        sbl_it_dao_sit1, sbl_it_dao_sit2, sbl_it_dao_sit3 = (
            SBLInstitutionTypeDao(id="1", name="Test SBL Instituion ID 1"),
            SBLInstitutionTypeDao(id="2", name="Test SBL Instituion ID 2"),
            SBLInstitutionTypeDao(id="13", name="Test SBL Instituion ID Other"),
        )

        sbl_type_mapping_dao1, sbl_type_mapping_dao2, sbl_type_mapping_dao3 = (
            SblTypeMappingDao(
                sbl_type=sbl_it_dao_sit1,
                lei="Test Bank 123",
                modified_by="test_user_id 1",
            ),
            SblTypeMappingDao(
                sbl_type=sbl_it_dao_sit2,
                lei="Test Bank 456",
                modified_by="test_user_id 2",
            ),
            SblTypeMappingDao(
                sbl_type=sbl_it_dao_sit3,
                lei="Test Sub Bank 456",
                modified_by="test_user_id 3",
            ),
        )

        fi_domain_dao1, fi_domain_dao2, fi_domain_dao3 = (
            FinancialInstitutionDomainDao(
                domain="sub.test.bank.1", lei="TESTBANK123000000000"
            ),
            FinancialInstitutionDomainDao(
                domain="sub.test.bank.2", lei="TESTBANK456000000000"
            ),
            FinancialInstitutionDomainDao(
                domain="sub.test.bank.2", lei="TESTSUBBANK456000000"
            ),
        )

        fi_dao_123, fi_dao_456, fi_dao_sub_456 = (
            FinancialInstitutionDao(
                name="Test Bank 123",
                lei="TESTBANK123000000000",
                is_active=True,
                domains=[fi_domain_dao1],
                tax_id="12-3456789",
                rssd_id=1234,
                primary_federal_regulator_id="FRI1",
                hmda_institution_type_id="HIT1",
                sbl_institution_types=[sbl_it_dao_sit1],
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
                is_active=True,
                domains=[fi_domain_dao2],
                tax_id="98-7654321",
                rssd_id=4321,
                primary_federal_regulator_id="FRI2",
                hmda_institution_type_id="HIT2",
                sbl_institution_types=[sbl_it_dao_sit2],
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
                is_active=True,
                domains=[fi_domain_dao3],
                tax_id="76-5432198",
                rssd_id=2134,
                primary_federal_regulator_id="FRI3",
                hmda_institution_type_id="HIT3",
                sbl_institution_types=[sbl_it_dao_sit3],
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

        transaction_session.add(sbl_it_dao_sit1)
        transaction_session.add(sbl_it_dao_sit2)
        transaction_session.add(sbl_it_dao_sit3)

        transaction_session.add(sbl_type_mapping_dao1)
        transaction_session.add(sbl_type_mapping_dao2)
        transaction_session.add(sbl_type_mapping_dao3)

        transaction_session.add(fi_domain_dao1)
        transaction_session.add(fi_domain_dao2)
        transaction_session.add(fi_domain_dao3)

        transaction_session.add(fi_dao_123)
        transaction_session.add(fi_dao_456)
        transaction_session.add(fi_dao_sub_456)
        transaction_session.commit()

    """def test_delete_domains_by_lei(self, session: Session):
        domains = institutions_repo.get_institution(session, "TESTBANK123000000000")
        res = repo.delete_domains_by_lei(session, "TESTBANK123000000000")

        pass

    def test_delete_sbl_type_by_lei():
        pass

    def test_delete_institution():
        pass"""

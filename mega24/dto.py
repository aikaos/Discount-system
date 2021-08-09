
from .models import View, SocialNetwork, Discount


class CompanyDto:
    pass


def get_company_dto(company):
    company_dto = CompanyDto()
    company_dto.id = company.id
    company_dto.logo = company.logo
    company_dto.name = company.name
    company_dto.working_hours = company.working_hours
    company_dto.city = company.address.city.name
    company_dto.percent = Discount.objects.get(id=company).percent
    company_dto.description = company.description
    company_dto.count = View.objects.get(id=company).count
    return company_dto


def get_company_dto_list(company_list):
    company_dto_list = []
    for company in company_list:
        company_dto = get_company_dto(company)
        company_dto_list.append(company_dto)
    return company_dto_list


def get_detail_dto(company):
    detail_dto = get_company_dto(company)
    detail_dto.street = company.address.street
    detail_dto.str_num = company.address.str_num
    detail_dto.lan = company.address.lan
    detail_dto.lon = company.address.lon
    detail_dto.condition = Discount.objects.get(id=company).condition
    detail_dto.social_networks = SocialNetwork.objects.filter(company=company)
    return detail_dto


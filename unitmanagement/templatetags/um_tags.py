from django import template
from planningandacquiring.models import Budget_allocation, Budget_medicine, Budget_equipment, Budget_food, Budget_vaccine, Budget_vet_supply
from inventory.models import Medicine

register = template.Library()



@register.filter
def list_item(List, i):

    return List[i]

@register.filter
def formset_item(formset, i):

    return formset.forms[i].fields['quantity']

@register.filter
def get_medicine_price(object, i):

    budget_med = Budget_medicine.objects.get(medicine = object)
    return budget_med.price

@register.filter
def get_medicine_quantity(object, i):

    budget_med = Budget_medicine.objects.get(medicine = object)
    return budget_med.quantity

@register.filter
def get_medicine_name(med_budget, i):

    med = Medicine.objects.get(id = med_budget.medicine.id)

    return med.medicine

@register.filter
def get_medicine_recent_price(med_budget_price_list, i):


    return med_budget_price_list[i]